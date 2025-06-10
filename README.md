# RisingWave MCP

A lightweight Model Context Protocol (MCP) server that lets you query and manage your RisingWave streaming database with natural language via AI assistants and tools.

## Features

- Real-time access to tables, materialized views, and streaming data
- Built on FastMCP and risingwave-py for high-performance STDIO transport
- Seamless integration with VS Code Copilot, Claude Desktop, and other MCP clients

## Installation

1. Clone the repository and enter the directory:

   ```bash
   git clone https://github.com/your-org/risingwave-mcp.git
   cd risingwave-mcp
   ```

2. Install runtime dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### VS Code Copilot

1. Create an MCP server in the VS Code Chat pane (Agent Mode → Select Tools).
2. Add or update `.vscode/mcp.json`:

   ```json
   {
     "servers": {
       "risingwave-mcp": {
         "type": "stdio",
         "command": "python",
         "args": ["path_to/risingwave-mcp/src/main.py"],
         "env": {
           "RISINGWAVE_CONNECTION_STR": "<risingwave-connection> or use connection params",
           "RISINGWAVE_HOST": "<risingwave-host>",
           "RISINGWAVE_USER": "<risingwave-user>",
           "RISINGWAVE_PORT": "4566",
           "RISINGWAVE_PASSWORD": "<risingwave-password>",
           "RISINGWAVE_DATABASE": "<risingwave-database>",
           "RISINGWAVE_SSLMODE": "require"
         }
       }
     }
   }
   ```

3. Start interacting in Chat; ask questions like "List my tables" or "Describe table users."

### Claude Desktop

Add to your `claude_desktop_config.json` under mcpServers:

```json
{
  "mcpServers": {
    "risingwave-mcp": {
      "command": "python",
      "args": ["path_to/risingwave-mcp/src/main.py"],
      "env": {
        "RISINGWAVE_CONNECTION_STR": "<risingwave-connection> or use connection params",
        "RISINGWAVE_HOST": "<risingwave-host>",
        "RISINGWAVE_USER": "<risingwave-user>",
        "RISINGWAVE_PORT": "4566",
        "RISINGWAVE_PASSWORD": "<risingwave-password>",
        "RISINGWAVE_DATABASE": "<risingwave-database>",
        "RISINGWAVE_SSLMODE": "require"
      }
    }
  }
}
```

Restart Claude Desktop to apply changes.

### Manual Testing

Run the server directly for development or CI:

```bash
python src/main.py
```

The server will listen on STDIN/STDOUT for MCP messages.

## Available Tools

- `list_databases` — List all databases
- `show_tables` — List tables in the current database
- `describe_table` — Describe table schema
- `run_select_query` — Safely execute SELECT queries
- `table_row_count` — Get row count for a table
- `check_table_exists` — Verify table existence
- `list_schemas` — List all schemas
- `list_materialized_views` — List materialized views
- `get_table_columns` — Detailed column info
- `create_materialized_view` — Create a new materialized view
- `drop_materialized_view` — Drop an existing view
- `execute_ddl_statement` — Run generic DDL commands
- `get_database_version` — Retrieve RisingWave version
- `flush_database` — Force flush pending writes

_For a full list, check `src/tools.py`._
