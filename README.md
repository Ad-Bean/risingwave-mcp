# RisingWave MCP

A Model Context Protocol (MCP) server for RisingWave database that provides seamless integration with AI assistants like Claude Desktop and VS Code Copilot. Built using FastMCP framework, this server enables natural language interactions with your RisingWave streaming database.

## Features

- **Real-time Database Access**: Query tables, materialized views, and streaming data
- **Comprehensive Tools**: 20+ MCP tools covering DDL, DML, and administrative operations
- **Security**: Environment-based configuration with credential protection
- **FastMCP Framework**: High-performance STDIO transport protocol
- **AI Assistant Integration**: Works with Claude Desktop, VS Code Copilot, and other MCP clients
- **Streaming Database Support**: Specialized tools for RisingWave's streaming capabilities

## Quick Start

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your RisingWave connection details
   ```

3. **Test the Server**:
   ```bash
   python src/main.py
   # Server starts and waits for MCP protocol messages
   ```

### Prerequisites

- Python 3.8 or higher
- Access to a RisingWave database instance
- VS Code (for VS Code Copilot integration) or Claude Desktop

### Step-by-Step Setup

1. **Clone and Install**:

   ```bash
   git clone <repository-url>
   cd risingwave-mcp
   pip install -r requirements.txt
   ```

1. **Environment Configuration**: Copy the template and configure your database connection:

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file with your actual RisingWave connection details:

   ```env
   RISINGWAVE_CONNECTION_STR=postgresql://username:password@host:port/database?sslmode=require
   ```

## Usage & Integration

This MCP server uses the STDIO transport protocol and integrates with various AI assistants. Choose your preferred integration method:

### 🔵 VS Code Copilot Integration

Perfect for developers who want database assistance while coding.

1. **Create MCP Server**: Click Agent Mode and Select Tools on VSCode Chat Pannel to start your MCP sever.

2. **Configure MCP Server**: Modify `.vscode/mcp.json` in your workspace:

   ```json
   {
     "servers": {
       "risingwave-mcp": {
         "type": "stdio",
         "command": "python",
         "args": ["src/main.py"]
       }
     }
   }
   ```

3. Reference: [Use MCP servers in VS Code (Preview)](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)

### Option 2: Using with Claude Desktop

1. **Configure Claude Desktop**: Add the server configuration to your `claude_desktop_config.json`:

   **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   **Linux**: `~/.config/Claude/claude_desktop_config.json`

   ```json
   {
     "mcpServers": {
       "risingwave-mcp": {
         "command": "python",
         "args": ["Path to/risingwave-mcp/src/main.py"]
       }
     }
   }
   ```

2. **Restart Claude Desktop**: Close and reopen Claude Desktop to load the new MCP server.

3. Reference: [Claude MCP Server Developers](https://modelcontextprotocol.io/quickstart/user)

### Option 3: Manual Testing (Development)

For development and testing purposes, you can run the server directly:

```bash
python src/main.py
```

The server will start and listen for MCP protocol messages on STDIN/STDOUT.

## Available Tools

Once connected, you can use the following MCP tools:

- `list_databases` - List all databases in the RisingWave cluster
- `show_tables` - List all tables in the database
- `run_select_query` - Execute SELECT queries safely
- `describe_table` - Get table structure and column information
- `table_row_count` - Get row count for a specific table
- `check_table_exists` - Check if a table exists
- `list_schemas` - List all database schemas
- `list_materialized_views` - List all materialized views
- `get_table_columns` - Get detailed column information
- `create_materialized_view` - Create new materialized views
- `drop_materialized_view` - Drop materialized views
- `execute_ddl_statement` - Execute DDL statements (CREATE, ALTER, DROP)
- `get_database_version` - Get RisingWave version information
- `flush_database` - Force flush pending writes
- And many more...

## Example Interactions

Once the MCP server is running, you can ask questions like:

- "List all my tables"
- "Describe the my_purchases table"
- "How many materialized views do I have?"
- "Show me the row count for the ad_events table"
- "Create a materialized view that calculates daily sales totals"
