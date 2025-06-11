import os
from risingwave import RisingWave, RisingWaveConnOptions


connection_str = os.getenv("RISINGWAVE_CONNECTION_STR")


def check_environment_variables():
    global connection_str
    if connection_str is None:
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

        connection_str = f"postgresql://{risingwave_user}:{risingwave_password}@{risingwave_host}:{risingwave_port}/{risingwave_database}?sslmode={risingwave_sslmode}&connect_timeout={risingwave_timeout}"

    return connection_str


def setup_risingwave_connection() -> RisingWave:
    """Set up a connection to the RisingWave database."""
    try:
        rw = RisingWave(
            RisingWaveConnOptions(check_environment_variables())
        )
        return rw
    except Exception as e:
        raise ValueError(f"Failed to connect to RisingWave: {str(e)}")
