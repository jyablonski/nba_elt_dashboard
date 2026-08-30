from __future__ import annotations

import hmac
import logging

logger = logging.getLogger(__name__)

BEARER_PREFIX = "bearer "


def extract_bearer_token(authorization_header: str | None) -> str | None:
    """Pull the token out of an `Authorization: Bearer <token>` header."""
    if not authorization_header:
        return None
    if not authorization_header.lower().startswith(BEARER_PREFIX):
        return None
    token = authorization_header[len(BEARER_PREFIX) :].strip()
    return token or None


def is_authorized(authorization_header: str | None, expected_token: str | None) -> bool:
    """Constant-time bearer check.

    An unset `expected_token` denies everything: the endpoint is internet-facing, so
    "no token configured" must fail closed rather than open the query surface.
    """
    if not expected_token:
        return False
    provided = extract_bearer_token(authorization_header)
    if provided is None:
        return False
    return hmac.compare_digest(provided, expected_token)


class BearerTokenMiddleware:
    """Pure-ASGI bearer gate in front of the MCP app.

    ASGI-level (rather than Starlette's BaseHTTPMiddleware) so it never buffers the
    streamed POST+SSE responses the Streamable HTTP transport depends on.
    """

    def __init__(self, app, expected_token: str | None, exempt_paths: tuple[str, ...] = ()) -> None:
        self.app = app
        self.expected_token = expected_token
        self.exempt_paths = exempt_paths

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http" or scope.get("path", "") in self.exempt_paths:
            await self.app(scope, receive, send)
            return

        header = _header_value(scope.get("headers", []), b"authorization")
        if not is_authorized(header, self.expected_token):
            await _send_unauthorized(send, configured=bool(self.expected_token))
            return

        await self.app(scope, receive, send)


def _header_value(headers, name: bytes) -> str | None:
    for key, value in headers:
        if key.lower() == name:
            return value.decode("latin-1")
    return None


async def _send_unauthorized(send, *, configured: bool) -> None:
    if not configured:
        logger.error("MCP_AUTH_TOKEN is not configured; rejecting request")
    body = b'{"error":"unauthorized"}'
    await send(
        {
            "type": "http.response.start",
            "status": 401,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode()),
                (b"www-authenticate", b"Bearer"),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body})
