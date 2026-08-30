#!/bin/bash
# Fetch the semantic manifest the dbt repo publishes on deploy and stage it for the MCP
# image build. Consuming the published artifact keeps dbt itself out of this build.
#
# Set DBT_SEMANTIC_MANIFEST_URI to the published artifact (s3:// or https://). It is dbt's
# `target/semantic_manifest.json` — NOT `manifest.json`; MetricFlow parses the former.
#
# The dbt repo publishes both a rolling copy and a per-commit one:
#   s3://$BUCKET/prod/semantic_manifest.json                  <- rolling latest (no-cache)
#   s3://$BUCKET/prod/history/$GITHUB_SHA/semantic_manifest.json  <- pin to a dbt commit
# Point at the rolling key normally; use a history key to pin a known-good manifest.
#
# NOTE: this runs on the deploy VM, so the s3:// path needs the AWS CLI and read
# credentials there. If the VM has neither, publish via a presigned/public https URL
# instead — both schemes are handled below.
#
# Unset URI is not fatal: the MCP server boots without a manifest and serves the
# direct-read tools, reporting the reason on nba://data-freshness.

set -euo pipefail

DEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/docker/semantic"
DEST="${DEST_DIR}/semantic_manifest.json"
URI="${DBT_SEMANTIC_MANIFEST_URI:-}"

mkdir -p "$DEST_DIR"

# Download to a temp file and only move it into place once validated, so a rejected or
# truncated fetch can never leave a bad manifest staged for the next build. Same reason
# the stale copy goes first: a failed deploy must not silently bake yesterday's artifact.
rm -f "$DEST"
STAGED="$(mktemp)"
trap 'rm -f "$STAGED"' EXIT

if [ -z "$URI" ]; then
  echo "DBT_SEMANTIC_MANIFEST_URI is not set; building without a semantic manifest."
  echo "MCP tools will fall back to direct gold reads."
  exit 0
fi

case "$URI" in
  */manifest.json)
    # Easy mistake to make: dbt publishes both, but MetricFlow only parses the semantic one.
    echo "ERROR: $URI looks like dbt's manifest.json." >&2
    echo "MetricFlow needs target/semantic_manifest.json (different shape)." >&2
    exit 1
    ;;
esac

echo "Fetching semantic manifest from $URI..."
case "$URI" in
  s3://*)
    if ! command -v aws >/dev/null 2>&1; then
      echo "ERROR: aws CLI not found; needed for the s3:// URI $URI" >&2
      echo "Install it on this host or publish the manifest over https instead." >&2
      exit 1
    fi
    aws s3 cp "$URI" "$STAGED"
    ;;
  http://* | https://*) curl -fsSL "$URI" -o "$STAGED" ;;
  *) echo "Unsupported URI scheme: $URI" >&2; exit 1 ;;
esac

# A truncated download or an S3/HTML error page would otherwise fail at container startup;
# check both that it's JSON and that it's the semantic manifest rather than manifest.json.
python3 - "$STAGED" <<'PY'
import json, sys

with open(sys.argv[1]) as fh:
    manifest = json.load(fh)

if not isinstance(manifest.get("semantic_models"), list):
    sys.exit(
        "Fetched file is not a semantic manifest: `semantic_models` is not a list. "
        "dbt's manifest.json keys these by unique_id; publish target/semantic_manifest.json."
    )
if "project_configuration" not in manifest:
    sys.exit("Semantic manifest is missing `project_configuration` (time spines live there).")

models = [model.get("name") for model in manifest["semantic_models"]]
metrics = [metric.get("name") for metric in manifest.get("metrics", [])]
spines = manifest["project_configuration"].get("time_spines") or []
if not spines:
    sys.exit("Semantic manifest declares no time spine; MetricFlow will refuse to load it.")
print(f"  semantic models: {models}")
print(f"  metrics: {metrics}")
PY

mv "$STAGED" "$DEST"
# Docker COPY preserves the mode, and mktemp gives 0600 — which the image's non-root
# appuser could not read, silently degrading the server to direct-read tools.
chmod 644 "$DEST"
trap - EXIT
echo "Staged semantic manifest at $DEST"
