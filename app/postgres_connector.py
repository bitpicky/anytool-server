"""Holds Postgres DB Connector."""

from typing import Dict

import sqlalchemy
from sqlalchemy import inspect


class PostgresConnector:
    """Postgres DB Connector/Adaptor."""

    def __init__(self, connection_params: Dict[str, str]) -> None:
        self.connection_url = sqlalchemy.engine.url.URL(
            drivername="postgresql+psycopg2",
            host=connection_params.get("host", str()),
            username=connection_params.get("user", str()),
            password=connection_params.get("password", str()),
            database=connection_params.get("database", str()),
            port=connection_params.get("port", str()),
        )
        self.engine = sqlalchemy.create_engine(self.connection_url)

    def get_tables_in_db_schema(self, target_schema: str):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names(schema=target_schema)
        return tables
