import pytest

CONNECTION_PARAMS = {
    "host": "localhost",
    "username": "anytool_user",
    "password": "magical_password",
    "database": "anytool_test_db",
    "port": "5432",
}


@pytest.mark.parametrize(
    "target_schema, target_table, expectation",
    [
        pytest.param(
            "public",
            "nlp_classification_output",
            {
                "column_header": [
                    "id",
                    "item_description",
                    "predicted_item_label",
                    "reviewed_answer",
                ],
                "table_content": [
                    (1, "pizza", "food", None),
                    (2, "prosciutto di parma", "food", None),
                    (3, "prosecco", "alcohol", None),
                    (4, "Lamborghini", "unknown", None),
                    (5, "Ferrari", "unknown", None),
                ],
            },
            id="first_test",
        )
    ],
)
def test_show_table_contents(target_schema, target_table, expectation):
    from app.postgres_connector import PostgresConnector

    connection_details = {
        "host": "localhost",
        "username": "anytool_user",
        "password": "magical_password",
        "database": "anytool_test_db",
        "port": "5432",
    }
    c = PostgresConnector(connection_params=connection_details)
    results = c.show_table_contents(target_schema=target_schema, target_table=target_table)
    assert results["column_header"] == expectation["column_header"]
    assert results["table_content"] == expectation["table_content"]


def test_get_tables_in_db_schema():
    from app.postgres_connector import PostgresConnector

    connection_details = {
        "host": "localhost",
        "username": "anytool_user",
        "password": "magical_password",
        "database": "anytool_test_db",
        "port": "5432",
    }
    c = PostgresConnector(connection_params=connection_details)
    results = c.get_tables_in_db_schema("public")
    assert results == [
        "test_table",
        "nlp_classification_output",
        "nlp_classification_output_update",
    ]


def test_update_table():
    from app.postgres_connector import PostgresConnector

    connection_details = {
        "host": "localhost",
        "username": "anytool_user",
        "password": "magical_password",
        "database": "anytool_test_db",
        "port": "5432",
    }

    request = {
        "target_schema": "public",
        "target_table": "nlp_classification_output_update",
        "payload": [
            {"filter": {"id": 3}, "content": {"reviewed_answer": "new_content"}},
            {"filter": {"id": 4}, "content": {"reviewed_answer": "new_content_2"}},
        ],
    }
    c = PostgresConnector(connection_params=connection_details)
    rez = c.update_table(request["target_schema"], request["target_table"], request["payload"])
    assert rez is None


def test_get_schemas_in_db():
    from app.postgres_connector import PostgresConnector

    connection_details = {
        "host": "localhost",
        "username": "anytool_user",
        "password": "magical_password",
        "database": "anytool_test_db",
        "port": "5432",
    }
    c = PostgresConnector(connection_params=connection_details)
    rez = c.get_schemas_in_db()
    assert rez == ["information_schema", "public"]


@pytest.mark.parametrize(
    "sql_input, expectation",
    [
        pytest.param(
            "select * from public.nlp_classification_output",
            {
                "column_header": [
                    "id",
                    "item_description",
                    "predicted_item_label",
                    "reviewed_answer",
                ],
                "table_content": [
                    (1, "pizza", "food", None),
                    (2, "prosciutto di parma", "food", None),
                    (3, "prosecco", "alcohol", None),
                    (4, "Lamborghini", "unknown", None),
                    (5, "Ferrari", "unknown", None),
                ],
            },
            id="legit lower case",
        ),
        pytest.param(
            "SELECT * from public.nlp_classification_output",
            {
                "column_header": [
                    "id",
                    "item_description",
                    "predicted_item_label",
                    "reviewed_answer",
                ],
                "table_content": [
                    (1, "pizza", "food", None),
                    (2, "prosciutto di parma", "food", None),
                    (3, "prosecco", "alcohol", None),
                    (4, "Lamborghini", "unknown", None),
                    (5, "Ferrari", "unknown", None),
                ],
            },
            id="legit upper case",
        ),
        pytest.param(
            "select * from public.nlp_classification_output; drop table public.nlp_classification_output",
            {
                "column_header": [
                    "id",
                    "item_description",
                    "predicted_item_label",
                    "reviewed_answer",
                ],
                "table_content": [
                    (1, "pizza", "food", None),
                    (2, "prosciutto di parma", "food", None),
                    (3, "prosecco", "alcohol", None),
                    (4, "Lamborghini", "unknown", None),
                    (5, "Ferrari", "unknown", None),
                ],
            },
            id="illegal but escapted",
        ),
    ],
)
def test_return_result_from_raw_sql(sql_input, expectation):
    from app.postgres_connector import PostgresConnector

    c = PostgresConnector(connection_params=CONNECTION_PARAMS)
    payload = c.return_result_from_raw_sql(sql_input)
    assert payload["column_header"] == expectation["column_header"]
    assert payload["table_content"] == expectation["table_content"]


@pytest.mark.parametrize(
    "sql_input",
    [
        pytest.param(
            "drop table public.nlp_classification_output",
            id="legit lower case",
        )
    ],
)
def test_return_result_from_raw_sql_illegal(sql_input):
    from app.postgres_connector import PostgresConnector

    c = PostgresConnector(connection_params=CONNECTION_PARAMS)
    with pytest.raises(NotImplementedError):
        payload = c.return_result_from_raw_sql(sql_input)
