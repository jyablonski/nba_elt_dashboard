from __future__ import annotations

import pytest


@pytest.fixture
def dashboard_app():
    """Import the app after the session database snapshot is ready."""
    from src.server import app

    return app
