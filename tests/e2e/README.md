# End-to-end tests (optional — Phase 7d)

Browser E2E is **not** run in CI by default: it needs a webdriver and a running app or Dash testing fixtures.

To experiment locally:

1. Ensure **`dash[testing]`** is installed (`uv sync --group test`).
2. Install a compatible **Chrome** / **chromedriver** (or use the driver managed by your Selenium setup).
3. Run with the gate enabled:

```bash
RUN_E2E=1 uv run pytest tests/e2e -m e2e -v
```

Add real tests with the **`dash_duo`** fixture when you want coverage of tab switches and callbacks in a headless browser.
