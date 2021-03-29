"""Holds Postgres DB Connector."""

from typing import Any, Dict, List, Mapping, Sequence, Tuple, Union

from sqlalchemy import MetaData, Table, and_, create_engine, engine, inspect, select, text
from sqlalchemy.orm import sessionmaker


class PostgresConnector:
    """Postgres DB Connector/Adaptor."""

    def __init__(self, connection_params: Dict[str, str]) -> None:
        self.connection_url = engine.URL.create(
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

    def get_schemas_in_db(self) -> List[str]:
        inspector = inspect(self.engine)
        schemas = inspector.get_schema_names()
        return schemas

    def show_table_contents(
        self, target_schema: str, target_table: str
    ) -> Dict[str, Sequence[Union[str, Tuple[Any]]]]:
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

    def update_table(
        self,
        target_schema: str,
        target_table: str,
        payload: Sequence[Mapping[str, Mapping[str, Any]]],
    ) -> None:
        metadata = MetaData(bind=None, schema=target_schema)
        metadata.reflect(bind=self.engine, only=["nlp_classification_output"])
        table = Table(target_table, metadata, autoload=True, autoload_with=self.engine)

        Session = sessionmaker(bind=self.engine)
        session = Session()

        for record in payload:
            stmt = (
                table.update()
                .where(and_(*[table.c[key] == value for key, value in record["filter"].items()]))
                .values(record["content"])
            )
            session.execute(stmt)
        session.commit()

    def return_result_from_raw_sql(
        self, sql_string: str
    ) -> Dict[str, Sequence[Union[str, Tuple[Any]]]]:
        # do some hacky injection protection
        _sql_string = sql_string.lower().strip().split(";")[0]
        if not _sql_string.startswith("select"):
            raise NotImplementedError("User provided statement that can only ve a SELECT statement")

        _sql_string = text(_sql_string)

        connection = self.engine.connect()

        results = connection.execute(_sql_string)
        column_header = list(results.keys())
        table_content = results.all()
        payload = {"column_header": column_header, "table_content": table_content}
        return payload
