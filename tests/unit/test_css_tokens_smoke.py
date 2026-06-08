from pathlib import Path


def _styles_css() -> Path:
    return Path(__file__).resolve().parents[2] / "static" / "styles.css"


def _tab_shell_css() -> Path:
    return Path(__file__).resolve().parents[2] / "static" / "tab_shell.css"


def test_global_css_defines_token_block_and_shell_hooks():
    text = _styles_css().read_text(encoding="utf-8")
    for needle in (
        ":root",
        "--bg:",
        "--accent:",
        "--font-sans:",
        "--font-display:",
        ".app-shell",
    ):
        assert needle in text, f"missing {needle!r} in static/styles.css"


def test_tab_shell_css_scopes_shell_tabs():
    text = _tab_shell_css().read_text(encoding="utf-8")
    assert ".nba-shell-tabs" in text, "missing shell tab scope in static/tab_shell.css"
