"""API Entry Point"""
from typing import Any, Dict, List, Sequence

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from postgres_connector import PostgresConnector
from pydantic import BaseModel


class TableKeyError(Exception):
    """Thrown when a key error is emited by the table updater."""

    def __init__(self, message: Exception):
        self.message = message


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SchemaRequest(BaseModel):
    """Pydantic model to validate request."""

    schema_name: str = "public"


class GreetingModel(BaseModel):
    """Pydandict greeting validation model."""

    name: str


class GreetingResult(BaseModel):
    """Pydandict model to validate response."""

    message: str


class ListOfTables(BaseModel):
    """Pydandic list of  tables validation model."""

    tables: List[str]


class TableContent(BaseModel):
    """Pydandict model for table content endpoint response validation."""

    column_header: List[str]
    table_content: List[Any]


class TableContentRequest(BaseModel):
    """Pydantic model for a table content request."""

    target_schema: str = "public"
    target_table: str = "nlp_classification_output"


@app.exception_handler(TableKeyError)
async def table_key_exception_handler(request: Request, exc: TableKeyError):
    """Raises a custom TableKeyError."""
    return JSONResponse(
        status_code=400,
        content={
            "message": "Oops! One of the update keys isn't found in the table. "
            f"Internal Error: {exc.message!r}"
        },
    )


@app.get("/")
async def root():
    """Basic Hello World."""
    return {"message": "Hello Hello World"}


@app.post("/greet", response_model=GreetingResult, name="greet by name")
def greet_by_name(request: GreetingModel) -> GreetingResult:
    """Takes a json with a name and returns a json with name greeted."""
    name = request.dict()["name"]
    return GreetingResult(**{"message": f"Hello Hello {name}"})


@app.post("/tables", response_model=ListOfTables, name="Tables in Schema")
def return_tables_in_schema(
    request: SchemaRequest,
) -> ListOfTables:
    """Returns a list of tables given a schema name in the database.

    Args:
        request (SchemaRequest): json payload of shape e.g: {"schema_name": "public"}

    Returns:
        ListOfTables: json payload of shape {"tables": ["list", "of", "tables"]}
    """
    connector = PostgresConnector(
        {
            "host": "localhost",
            "username": "anytool_user",
            "password": "magical_password",
            "database": "anytool_test_db",
            "port": "5432",
        }
    )
    tables = connector.get_tables_in_db_schema(target_schema=request.dict()["schema_name"])
    return ListOfTables(**{"tables": tables})


@app.post("/table_content", response_model=TableContent, name="Table Content")
def return_table_content(request: TableContentRequest) -> TableContent:
    """Dummy"""
    connector = PostgresConnector(
        {
            "host": "localhost",
            "username": "anytool_user",
            "password": "magical_password",
            "database": "anytool_test_db",
            "port": "5432",
        }
    )
    table_content_payload = connector.show_table_contents(
        target_schema=request.dict()["target_schema"],
        target_table=request.dict()["target_table"],
    )
    return table_content_payload


class UpdateTablePayload(BaseModel):
    """Validation Schema for the payload part of an update request."""

    filter: Dict[str, Any] = {"id": 3}
    content: Dict[str, Any] = {"reviewed_answer": "yummy"}


class UpdateTableRequest(BaseModel):
    """Validation schema for the update table request."""

    target_schema: str = "public"
    target_table: str = "nlp_classification_output"
    payload: Sequence[UpdateTablePayload]


@app.put("/update_table", name="Update Table Content")
def update_table_content(request: UpdateTableRequest):
    """Updates a table with new content."""
    connector = PostgresConnector(
        {
            "host": "localhost",
            "username": "anytool_user",
            "password": "magical_password",
            "database": "anytool_test_db",
            "port": "5432",
        }
    )
    try:
        connector.update_table(
            target_schema=request.dict()["target_schema"],
            target_table=request.dict()["target_table"],
            payload=request.dict()["payload"],
        )
    except KeyError as e:
        raise TableKeyError(message=e)
