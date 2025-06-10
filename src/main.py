from fastmcp import FastMCP
import os
from risingwave import RisingWave, RisingWaveConnOptions, OutputFormat

mcp = FastMCP("Risingwave MCP Server")

CONNECTION_STR = os.getenv("RISINGWAVE_CONNECTION_STR")

if CONNECTION_STR is None :
    risingwave_host = os.getenv("RISINGWAVE_HOST")
    risingwave_user = os.getenv("RISINGWAVE_USER")
    risingwave_password = os.getenv("RISINGWAVE_PASSWORD")
    risingwave_port = os.getenv("RISINGWAVE_PORT", "4566")
    risingwave_database = os.getenv("RISINGWAVE_DATABASE", "dev")
    risingwave_sslmode = os.getenv("RISINGWAVE_SSLMODE", "require")
    risingwave_timeout = os.getenv("RISINGWAVE_TIMEOUT", "30")

    if not risingwave_host or not risingwave_user or not risingwave_password:
        raise ValueError(
            "RISINGWAVE_HOST, RISINGWAVE_USER, and RISINGWAVE_PASSWORD must be set in environment variables")

    CONNECTION_STR = f"postgresql://{risingwave_user}:{risingwave_password}@{risingwave_host}:{risingwave_port}/{risingwave_database}?sslmode={risingwave_sslmode}&connect_timeout={risingwave_timeout}"

def setup_risingwave_connection():
    """Set up a connection to the RisingWave database."""
    try:
        rw = RisingWave(
            RisingWaveConnOptions(CONNECTION_STR)
        )
        return rw
    except Exception as e:
        raise ValueError(f"Failed to connect to RisingWave: {str(e)}")



@mcp.tool
def show_tables() -> str:
    """List all tables in the database."""
    rw = setup_risingwave_connection()
    result = rw.fetch("SHOW TABLES", format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def list_databases() -> str:
    """List all databases in the RisingWave cluster."""
    rw = setup_risingwave_connection()
    result = rw.fetch("SHOW DATABASES", format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def run_select_query(query: str) -> str:
    """
    Execute a SELECT query against the RisingWave database.

    Args:
        query: The SELECT SQL query to execute (must start with SELECT)

    Returns:
        Query results as a formatted string
    """
    # Security check: only allow SELECT queries
    query_upper = query.strip().upper()
    if not query_upper.startswith('SELECT'):
        raise ValueError(
            "Only SELECT queries are allowed for security reasons")

    rw = setup_risingwave_connection()
    result = rw.fetch(query, format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def describe_table(table_name: str) -> str:
    """
    Describe the structure of a table (columns, types, etc.).

    Args:
        table_name: Name of the table to describe

    Returns:
        Table structure information
    """
    rw = setup_risingwave_connection()
    query = f"DESCRIBE {table_name}"
    result = rw.fetch(query, format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def describe_materialized_view(mv_name: str) -> str:
    """
    Describe the structure of a materialized view (columns, types, etc.).

    Args:
        mv_name: Name of the table to describe

    Returns:
        Table structure information
    """
    rw = setup_risingwave_connection()
    query = f"DESCRIBE {mv_name}"
    result = rw.fetch(query, format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def show_create_table(table_name: str) -> str:
    """
    Show the CREATE TABLE statement for a specific table.

    Args:
        table_name: Name of the table

    Returns:
        CREATE TABLE statement
    """
    rw = setup_risingwave_connection()
    query = f"SHOW CREATE TABLE {table_name}"
    result = rw.fetch(query, format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def show_create_materialized_view(mv_name: str) -> str:
    """
    Show the CREATE MATERIALIZED VIEW statement for a specific materialized view.

    Args:
        mv_name: Name of the materialized view

    Returns:
        CREATE MATERIALIZED VIEW statement
    """
    rw = setup_risingwave_connection()
    query = f"SHOW CREATE MATERIALIZED VIEW {mv_name}"
    result = rw.fetch(query, format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def table_row_count(table_name: str) -> str:
    """
    Get the row count for a specific table.

    Args:
        table_name: Name of the table

    Returns:
        Row count as a string
    """
    rw = setup_risingwave_connection()
    query = f"SELECT COUNT(*) as row_count FROM {table_name}"
    result = rw.fetch(query, format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def check_table_exists(table_name: str, schema_name: str = "public") -> str:
    """
    Check if a table or materialized view exists in the specified schema.

    Args:
        table_name: Name of the table to check
        schema_name: Name of the schema (default: "public")

    Returns:
        Boolean result as string indicating if table exists
    """
    rw = setup_risingwave_connection()
    exists = rw.check_exist(name=table_name, schema_name=schema_name)
    return f"Table '{table_name}' in schema '{schema_name}' exists: {exists}"


@mcp.tool
def list_schemas() -> str:
    """
    List all schemas in the RisingWave database.

    Returns:
        List of schemas as a formatted string
    """
    rw = setup_risingwave_connection()
    result = rw.fetch(
        "SELECT schema_name FROM information_schema.schemata", format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def list_materialized_views() -> str:
    """
    List all materialized views in a specific schema.

    Args:
        schema_name: Name of the schema (default: "public")

    Returns:
        List of materialized views
    """
    rw = setup_risingwave_connection()
    query = "SHOW MATERIALIZED VIEWS"
    result = rw.fetch(query, format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def get_table_columns(table_name: str, schema_name: str = "public") -> str:
    """
    Get detailed column information for a table.

    Args:
        table_name: Name of the table
        schema_name: Name of the schema (default: "public")

    Returns:
        Column details including names, types, and constraints
    """
    rw = setup_risingwave_connection()
    query = f"""
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns 
    WHERE table_name = '{table_name}' AND table_schema = '{schema_name}'
    ORDER BY ordinal_position
    """
    result = rw.fetch(query, format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def create_materialized_view(name: str, sql_statement: str, schema_name: str = "public") -> str:
    """
    Create a new materialized view.

    Args:
        name: Name of the materialized view
        sql_statement: SQL statement for the materialized view
        schema_name: Schema name (default: "public")

    Returns:
        Success message
    """
    rw = setup_risingwave_connection()
    try:
        rw.mv(name=name, stmt=sql_statement, schema_name=schema_name)
        return f"Materialized view '{name}' created successfully in schema '{schema_name}'"
    except Exception as e:
        return f"Error creating materialized view: {str(e)}"


@mcp.tool
def drop_materialized_view(name: str, schema_name: str = "public") -> str:
    """
    Drop a materialized view.

    Args:
        name: Name of the materialized view to drop
        schema_name: Schema name (default: "public")

    Returns:
        Success or error message
    """
    rw = setup_risingwave_connection()
    try:
        query = f"DROP MATERIALIZED VIEW {schema_name}.{name}"
        rw.execute(query)
        return f"Materialized view '{name}' dropped successfully from schema '{schema_name}'"
    except Exception as e:
        return f"Error dropping materialized view: {str(e)}"


@mcp.tool
def execute_ddl_statement(sql_statement: str) -> str:
    """
    Execute a DDL (Data Definition Language) statement like CREATE TABLE, CREATE SCHEMA, etc.

    Args:
        sql_statement: The DDL SQL statement to execute

    Returns:
        Success or error message
    """
    # Security check: only allow DDL statements
    sql_upper = sql_statement.strip().upper()
    allowed_ddl = ['CREATE', 'ALTER', 'DROP', 'TRUNCATE']

    if not any(sql_upper.startswith(keyword) for keyword in allowed_ddl):
        raise ValueError(
            "Only DDL statements (CREATE, ALTER, DROP, TRUNCATE) are allowed")

    # Additional security: prevent dangerous operations
    dangerous_keywords = ['DROP DATABASE', 'DROP SCHEMA', 'TRUNCATE']
    if any(keyword in sql_upper for keyword in dangerous_keywords):
        raise ValueError("Dangerous DDL operations are not allowed")

    rw = setup_risingwave_connection()
    try:
        rw.execute(sql_statement)
        return f"DDL statement executed successfully: {sql_statement[:100]}..."
    except Exception as e:
        return f"Error executing DDL statement: {str(e)}"


@mcp.tool
def get_database_version() -> str:
    """
    Get the RisingWave database version information.

    Returns:
        Database version information
    """
    rw = setup_risingwave_connection()
    result = rw.fetchone("SELECT version()", format=OutputFormat.DATAFRAME)
    return result


@mcp.tool
def list_subscriptions(schema_name: str = "public") -> str:
    """
    List all subscriptions in a specific schema.

    Args:
        schema_name: Name of the schema (default: "public")

    Returns:
        List of subscriptions
    """
    rw = setup_risingwave_connection()
    query = f"SHOW SUBSCRIPTIONS FROM {schema_name}"
    try:
        result = rw.fetch(query, format=OutputFormat.DATAFRAME)
        return result
    except Exception as e:
        return f"Error listing subscriptions: {str(e)}"


@mcp.tool
def get_table_stats(table_name: str, schema_name: str = "public") -> str:
    """
    Get comprehensive statistics for a table.

    Args:
        table_name: Name of the table
        schema_name: Name of the schema (default: "public")

    Returns:
        Table statistics including row count and column information
    """
    rw = setup_risingwave_connection()

    # Get row count
    row_count_query = f"SELECT COUNT(*) as row_count FROM {schema_name}.{table_name}"
    row_count = rw.fetchone(row_count_query, format=OutputFormat.DATAFRAME)

    # Get column info
    column_query = f"""
    SELECT 
        COUNT(*) as column_count,
        STRING_AGG(column_name, ', ') as column_names
    FROM information_schema.columns 
    WHERE table_name = '{table_name}' AND table_schema = '{schema_name}'
    """
    column_info = rw.fetchone(column_query, format=OutputFormat.DATAFRAME)

    # Combine results
    stats = {
        "table": f"{schema_name}.{table_name}",
        "row_count": row_count,
        "column_info": column_info
    }

    return str(stats)


@mcp.tool
def insert_single_row(table_name: str, column_data: str, schema_name: str = "public") -> str:
    """
    Insert a single row into a table.

    Args:
        table_name: Name of the table
        column_data: JSON string of column names and values (e.g., '{"col1": "value1", "col2": 123}')
        schema_name: Name of the schema (default: "public")

    Returns:
        Success or error message
    """
    import json
    rw = setup_risingwave_connection()
    try:
        # Parse the JSON column data
        column_values = json.loads(column_data)
        rw.insert_row(
            table_name=table_name,
            schema_name=schema_name,
            force_flush=True,
            **column_values
        )
        return f"Row inserted successfully into {schema_name}.{table_name}"
    except json.JSONDecodeError:
        return "Error: column_data must be valid JSON format"
    except Exception as e:
        return f"Error inserting row: {str(e)}"


@mcp.tool
def show_running_queries() -> str:
    """
    Show currently running queries (if supported by RisingWave version).

    Returns:
        List of running queries or error message
    """
    rw = setup_risingwave_connection()
    try:
        # This may not be available in all RisingWave versions
        result = rw.fetch("SHOW PROCESSLIST", format=OutputFormat.DATAFRAME)
        return result
    except Exception as e:
        return f"Show running queries not supported or error occurred: {str(e)}"


@mcp.tool
def flush_database() -> str:
    """
    Force flush all pending writes to the database.

    Returns:
        Success message
    """
    rw = setup_risingwave_connection()
    try:
        rw.execute("FLUSH")
        return "Database flush completed successfully"
    except Exception as e:
        return f"Error flushing database: {str(e)}"


@mcp.tool
def list_table_privileges(table_name: str, schema_name: str = "public") -> str:
    """
    List privileges for a specific table.

    Args:
        table_name: Name of the table
        schema_name: Name of the schema (default: "public")

    Returns:
        Table privileges information
    """
    rw = setup_risingwave_connection()
    query = f"""
    SELECT grantee, privilege_type, is_grantable
    FROM information_schema.table_privileges 
    WHERE table_name = '{table_name}' AND table_schema = '{schema_name}'
    """
    try:
        result = rw.fetch(query, format=OutputFormat.DATAFRAME)
        return result
    except Exception as e:
        return f"Error getting table privileges: {str(e)}"


if __name__ == "__main__":

    mcp.run(transport="stdio")
