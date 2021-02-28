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
    assert results == ["test_table", "nlp_classification_output"]
