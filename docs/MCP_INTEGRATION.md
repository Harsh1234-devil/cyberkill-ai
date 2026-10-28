# Model Context Protocol (MCP) Integration Guide

Cyberkill.ai natively implements Anthropic's Model Context Protocol (MCP), allowing AI assistants (Claude Desktop, Cursor, Roo Code, VS Code Copilot) to execute real-time cybersecurity tools.

## Claude Desktop Configuration
Add the following to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "cyberkill-ai": {
      "command": "python3",
      "args": [
        "-m",
        "cyberkill.mcp_server"
      ],
      "env": {
        "PYTHONPATH": "/path/to/cyberkill-ai/src"
      }
    }
  }
}
```

## Cursor IDE Configuration
In `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "cyberkill": {
      "command": "cyberkill-mcp"
    }
  }
}
```
