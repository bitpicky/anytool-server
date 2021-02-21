"""API Entry Point"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class GreetingModel(BaseModel):
    """Pydantic model to validate request."""

    name: str


class GreetingResult(BaseModel):
    """Pydandict model to validate response."""

    message: str


@app.get("/")
async def root():
    """Basic Hello World."""
    return {"message": "Hello Hello World"}


@app.post("/greet", response_model=GreetingResult, name="greet by name")
def greet_by_name(request: GreetingModel) -> GreetingResult:
    """Takes a json with a name and returns a json with name greeted."""
    name = request.dict()["name"]
    return GreetingResult(**{"message": f"Hello Hello {name}"})
