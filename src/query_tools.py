from risingwave import OutputFormat
from connection import setup_risingwave_connection


def run_select_query(query: str) -> str:
    """
    Execute a SELECT query against the RisingWave database.

    Args:
        query: The SELECT SQL query to execute (must start with SELECT)

    Returns:
        Query results as a formatted string
    """
    query_upper = query.strip().upper()
    if not query_upper.startswith('SELECT'):
        raise ValueError(
            "Only SELECT queries are allowed for security reasons")

    rw = setup_risingwave_connection()
    result = rw.fetch(query, format=OutputFormat.DATAFRAME)
    return result


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

    row_count_query = f"SELECT COUNT(*) as row_count FROM {schema_name}.{table_name}"
    row_count = rw.fetchone(row_count_query, format=OutputFormat.DATAFRAME)

    column_query = f"""
    SELECT 
        COUNT(*) as column_count,
        STRING_AGG(column_name, ', ') as column_names
    FROM information_schema.columns 
    WHERE table_name = '{table_name}' AND table_schema = '{schema_name}'
    """
    column_info = rw.fetchone(column_query, format=OutputFormat.DATAFRAME)

    stats = {
        "table": f"{schema_name}.{table_name}",
        "row_count": row_count,
        "column_info": column_info
    }

    return str(stats)
