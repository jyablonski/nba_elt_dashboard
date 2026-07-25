"""MCP server exposing the NBA `gold` schema as LLM-callable tools.

Runs as its own container/process (see `docker/Dockerfile.mcp`); it deliberately shares
nothing with the Dash app at runtime beyond the `src.data_access` config helpers.
"""
