# Airsoft Club Backend

This is the backend component of the Airsoft Club project.

## Prerequisites

Before running the application, make sure you have the following installed:

- Pyenv
- PostgreSQL
- Docker

## Installation

1. Clone the repository:

```shell
git clone git@github.com:AirsoftClub/airsoftclub.git
cd airsoftclub/
```

2. Create your venv:
```shell
pyenv install 3.12.1
pyenv virtualenv 3.12.1 airsoftclub-3.12.1
```


3. Install the required dependencies:

```shell
pip install poetry
poetry install
```

4. Enable pre-commits:
```shell
pip install pre-commit
pre-commit install --hook-type pre-push
pre-commit autoupdate
```

5. Setup the database:

```shell
setup/setup_db.sh
```

6. Run the uvicorn:

```shell
uvicorn main:create_app --reload --factory
```

## Testing

To run the tests execute:

```shell
pytest
```

If you want to run tests in parallel run:

```shell
pytest -n 4
```

Or:

```shell
pytest -n auto
```
