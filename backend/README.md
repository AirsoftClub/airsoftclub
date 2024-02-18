# Airsoft Club Backend

![Python Version](https://img.shields.io/badge/python-3.12.1-blue.svg) ![PostgreSQL Version](https://img.shields.io/badge/PostgreSQL-16.1-blue.svg) ![Docker](https://img.shields.io/badge/docker-latest-blue.svg)

This is the backend component of the Airsoft Club project, designed to provide RESTful APIs for the Airsoft Club application.

## 📋 Prerequisites

Before running the application, ensure you have the following installed:
- [Pyenv](https://github.com/pyenv/pyenv)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Docker](https://www.docker.com/products/docker-desktop)

## 🚀 Installation

Follow these steps to get your development environment set up:

1. **Clone the repository**:
    ```shell
    git clone git@github.com:AirsoftClub/airsoftclub.git
    cd airsoftclub/backend
    ```

2. **Create your Python virtual environment**:
    ```shell
    pyenv install 3.12.1
    pyenv virtualenv 3.12.1 airsoftclub-3.12.1
    ```

3. **Install the required dependencies**:
    ```shell
    pip install poetry
    poetry install
    ```

4. **Enable pre-commits and run initial checks**:
    ```shell
    pip install pre-commit
    pre-commit install --hook-type pre-commit
    pre-commit run --all-files
    ```

5. **Setup the database**:
    ```shell
    ./setup/setup_db.sh
    ```

6. **Run the application using uvicorn**:
    ```shell
    uvicorn main:create_app --reload --factory --host 0.0.0.0
    ```

## 🧪 Testing

To ensure the quality of the code, follow these steps to run the tests:

- **Run unit tests serially**:
    ```shell
    pytest
    ```

- **Run unit tests in parallel**:
    For faster execution, you can run tests in parallel:
    ```shell
    pytest -n 4
    ```
    Or, to automatically use as many workers as the number of CPUs:
    ```shell
    pytest -n auto
    ```

- **Run system tests**:
    ```shell
    behave
    ```

## 📦 Docker Support

This project includes Docker support for easy development and deployment. To build and run the application using Docker, use:
```shell
docker-compose up --build
```
