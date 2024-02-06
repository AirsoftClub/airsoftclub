# Airsoft Club Backend

This is the backend component of the Airsoft Club project.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- PostgreSQL
- Docker

## Installation

1. Clone the repository:

```shell
git clone https://github.com/your-username/airsoftclub-backend.git
```

2. Install the required dependencies:

```shell
pip install poetry
poetry install
```

3. Setup the database:

```shell
setup/build.sh
```

4. Run the uvicorn:

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
