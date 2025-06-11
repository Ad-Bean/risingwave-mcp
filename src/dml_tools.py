from fastmcp import FastMCP
from connection import setup_risingwave_connection


def register_dml_tools(mcp: FastMCP):
    """Register all DML-related MCP tools"""

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
