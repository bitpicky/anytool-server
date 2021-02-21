[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/bitpicky/anytool-server/main.svg)](https://results.pre-commit.ci/latest/github/bitpicky/anytool-server/main)

# anytool-server

Backend code for anytool web-app that allows humans to build quick front-ends on top of their database tables.

## Local Setup

- create a virtual environment with python 3.8.7
- activate that environment and install requirements

```bash
pip install -r requirements.txt
```

- Spin up postgres container to have a local db

```
cd tests/postgres_db
docker-compose up -V
```

- This will create a test db that is exposed on `localhost` port `5432`

- Open a new terminal (don't close the previous one unless you composed the docker in `-d` mode)
- Spin up `FastAPI` backend:

```bash
cd app
uvicorn main:app --reload
```

- This should work and expose the address and port to which you can send requests.
- To get the API documentation with all the endpoints and request/response schemas you can http to http://localhost:8000/docs which should look kinda nice already.

- When you're done testing you can tear down the backend server via `ctrl + c`
- Exit the docker container terminal `ctrl + c` and kill the docker container with `docker-compose down -v`
