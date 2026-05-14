"""Reserved for dash_duo / browser E2E; skipped unless RUN_E2E=1."""

from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.e2e


@pytest.mark.skipif(
    os.environ.get("RUN_E2E") != "1",
    reason="Set RUN_E2E=1 and configure a browser driver (see tests/e2e/README.md).",
)
def test_e2e_gate_documented():
    assert os.environ["RUN_E2E"] == "1"
