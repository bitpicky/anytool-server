import pytest


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
