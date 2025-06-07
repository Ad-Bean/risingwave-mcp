# RisingWave MCP

RisingWave MCP is a project that provides a framework for managing connections and executing queries against the RisingWave database using FastMCP. This project is inspired by the Postgres MCP and aims to facilitate seamless interaction with the RisingWave database.

## Features

- Connection management to the RisingWave database.
- Execution of SQL queries with easy-to-use functions.
- Built using FastMCP for efficient processing.

## Installation

To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Configuration

1. **Environment Variables**: Copy the `.env.example` file to `.env` and update it with your RisingWave database connection details:

   ```
   cp .env.example .env
   ```

   Then edit the `.env` file and set your actual connection string:

   ```
   RISINGWAVE_CONNECTION_STR=postgresql://username:password@host:port/database?sslmode=require
   ```

   **Note**: The `.env` file is already included in `.gitignore` to prevent accidentally committing sensitive credentials.

## Usage

1. **Initialize the Application**: Start by running the `main.py` file, which serves as the entry point for the application.

   ```
   python src/main.py
   ```

2. **Connect to the Database**: Use the `ConnectionManager` class from `src/tools/connection.py` to establish a connection to the RisingWave database.

3. **Execute Queries**: Utilize the functions in `src/tools/queries.py` to run SQL queries and fetch results.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.