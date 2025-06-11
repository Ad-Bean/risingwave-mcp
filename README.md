# RisingWave MCP Server

**RisingWave MCP Server** is a lightweight [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server that lets you query and manage your [RisingWave](https://risingwave.com) streaming database using natural language through AI assistants like VS Code Copilot and Claude Desktop.

---

## 🚀 Features

- Real-time access to RisingWave tables, materialized views, and streaming data
- Built on [`FastMCP`](https://github.com/jlowin/fastmcp) and [`risingwave-py`](https://github.com/risingwavelabs/risingwave-py) with high-performance STDIO transport
- Seamless integration with VS Code Copilot, Claude Desktop, and other MCP-compatible tools

---

## 📦 Installation

```bash
git clone https://github.com/risingwavelabs/risingwave-mcp.git
cd risingwave-mcp
pip install -r requirements.txt
```

---

## ⚙️ Setting Up

You’ll need a running RisingWave instance—either locally or in the cloud.

### Option 1: Run RisingWave Locally

```bash
# Install RisingWave standalone
curl -L https://risingwave.com/sh | sh

# macOS
risingwave

# Linux
./risingwave
```

For Docker or other options, see the docs:
👉 [https://docs.risingwave.com/get-started/quickstart](https://docs.risingwave.com/get-started/quickstart)

### Option 2: Use RisingWave Cloud

You can also spin up a free-tier cluster in seconds:
👉 [https://cloud.risingwave.com/auth/signin](https://cloud.risingwave.com/auth/signin)

---

## 🧩 Integration

### VS Code Copilot

1. In the **VS Code Chat** panel: Agent Mode → Select Tools → Create MCP Server.
2. Add the following to `.vscode/mcp.json`.

#### ✅ Option 1: Use a connection string

```json
{
  "servers": {
    "risingwave-mcp": {
      "type": "stdio",
      "command": "python",
      "args": ["path_to/risingwave-mcp/src/main.py"],
      "env": {
        "RISINGWAVE_CONNECTION_STR": "postgresql://root:root@localhost:4566/dev"
      }
    }
  }
}
```

**Explanation:**

- `postgresql://` — Use PostgreSQL protocol (RisingWave is compatible)
- `root:root@` — Username and password
- `localhost:4566` — Host and port
- `/dev` — Database name

#### ✅ Option 2: Use individual parameters

```json
{
  "servers": {
    "risingwave-mcp": {
      "type": "stdio",
      "command": "python",
      "args": ["path_to/risingwave-mcp/src/main.py"],
      "env": {
        "RISINGWAVE_HOST": "localhost",
        "RISINGWAVE_PORT": "4566",
        "RISINGWAVE_USER": "root",
        "RISINGWAVE_PASSWORD": "root",
        "RISINGWAVE_DATABASE": "dev",
        "RISINGWAVE_SSLMODE": "disable"
      }
    }
  }
}
```

3. Start chatting!
   Ask questions like:

   - _"List my tables"_
   - _"Create a materialized view that aggregates payments by minute"_

---

### Claude Desktop

1. Add the MCP server to your `claude_desktop_config.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "risingwave-mcp": {
      "command": "python",
      "args": ["path_to/risingwave-mcp/src/main.py"],
      "env": {
        "RISINGWAVE_CONNECTION_STR": "postgresql://root:root@localhost:4566/dev"
      }
    }
  }
}
```

2. Restart Claude Desktop to apply changes.

---

### Manual Testing (Dev / CI)

You can run the MCP server directly from the CLI:

```bash
python src/main.py
```

This will listen for MCP messages over STDIN/STDOUT.

---

## 🛠️ Available Tools

| Tool Name                  | Description                                                          |
| -------------------------- | -------------------------------------------------------------------- |
| `list_databases`           | List all databases                                                   |
| `show_tables`              | List tables in the current database                                  |
| `describe_table`           | Describe the schema of a table                                       |
| `run_select_query`         | Safely execute a `SELECT` query                                      |
| `explain_query`            | Get query execution plan without running it                          |
| `explain_analyze`          | Get detailed execution statistics by running the query(only in v2.4) |
| `table_row_count`          | Return row count for a table                                         |
| `check_table_exists`       | Check whether a table exists                                         |
| `list_schemas`             | List all available schemas                                           |
| `list_materialized_views`  | List all materialized views                                          |
| `get_table_columns`        | Return detailed info about table columns                             |
| `create_materialized_view` | Create a new materialized view                                       |
| `drop_materialized_view`   | Drop an existing materialized view                                   |
| `execute_ddl_statement`    | Run generic DDL like `CREATE TABLE`                                  |
| `get_database_version`     | Return the current RisingWave version                                |
| `flush_database`           | Force flush any pending writes                                       |

For a full list of tools, see [`src/tools.py`](src/tools.py).
