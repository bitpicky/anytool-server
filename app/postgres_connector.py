"""Holds Postgres DB Connector."""

from typing import Dict

from sqlalchemy import MetaData, Table, create_engine, inspect, select
from sqlalchemy.engine import url


class PostgresConnector:
    """Postgres DB Connector/Adaptor."""

    def __init__(self, connection_params: Dict[str, str]) -> None:
        self.connection_url = url.URL(
            drivername="postgresql+psycopg2",
            host=connection_params.get("host", str()),
            username=connection_params.get("username", str()),
            password=connection_params.get("password", str()),
            database=connection_params.get("database", str()),
            port=connection_params.get("port", str()),
        )
        self.engine = create_engine(self.connection_url)

    def get_tables_in_db_schema(self, target_schema: str):
        inspector = inspect(self.engine)
        tables = inspector.get_table_names(schema=target_schema)
        return tables

    def show_table_contents(self, target_schema: str, target_table: str):
        metadata = MetaData(bind=None, schema=target_schema)
        table = Table(
            target_table,
            metadata,
            autoload=True,
            autoload_with=self.engine,
        )
        select_statement = select([table])
        connection = self.engine.connect()
        column_header = [column.name for column in table.columns]
        table_contents = connection.execute(select_statement).fetchall()
        payload = {"column_header": column_header, "table_content": table_contents}
        return payload
