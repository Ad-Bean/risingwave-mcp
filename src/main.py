from fastmcp import FastMCP
import threading
import os
from dotenv import load_dotenv
from risingwave import RisingWave, RisingWaveConnOptions, OutputFormat

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP("Risingwave MCP Server")

# Get connection string from environment variable
CONNECTION_STR = os.getenv("RISINGWAVE_CONNECTION_STR")

if not CONNECTION_STR:
    raise ValueError(
        "RISINGWAVE_CONNECTION_STR environment variable is not set. Please check your .env file.")


def setup_risingwave_connection():
    """Set up a connection to the RisingWave database."""
    rw = RisingWave(
        RisingWaveConnOptions(CONNECTION_STR)
    )
    return rw


@mcp.tool
def show_tables() -> str:
    """List all tables in the database."""
    rw = setup_risingwave_connection()
    result = rw.fetch("SHOW TABLES", format=OutputFormat.DATAFRAME)
    return result

    if __name__ == "__main__":
        mcp.run(transport="stdio")
