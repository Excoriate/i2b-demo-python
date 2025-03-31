# i2b-demo-python

FastAPI service using CouchDB, managed with uv.

## Overview

This project provides a basic structure for a Python API service built with FastAPI, using CouchDB as the database, `uv` for package management, and `just` as a task runner. It includes Docker support for containerization.

## Setup

1.  **Environment Variables:** Copy the `.env.example` file to `.env` and fill in your specific configuration values:
    ```bash
    cp .env.example .env
    # Edit .env with your details
    ```
2.  **Install Dependencies:** Create the virtual environment (if needed) and install dependencies using `just`:
    ```bash
    just install
    ```

## Running the Application

*   **Locally:** Use the `just` command:
    ```bash
    just run
    ```
    The API will be available at `http://<APP_HOST>:<APP_PORT>` (e.g., `http://0.0.0.0:8000`).

*   **With Docker Compose:** Use the `just` command (ensure Docker Desktop or Docker Engine is running):
    ```bash
    just compose-up
    ```
    This will build the images (if necessary) and start the `app` and `db` services defined in `compose.yaml`. The API will be available at `http://localhost:8000`. To stop the services:
    ```bash
    just compose-down
    ```

## Environment Variables

The application requires the following environment variables to be set (either in your shell or in a `.env` file):

| Variable         | Description                                      | Example Value             |
|------------------|--------------------------------------------------|---------------------------|
| `COUCHDB_URL`    | URL for the CouchDB instance                     | `http://localhost:5984/`  |
| `COUCHDB_USER`   | Username for CouchDB authentication              | `admin`                   |
| `COUCHDB_PASSWORD`| Password for CouchDB authentication              | `password`                |
| `COUCHDB_DB_NAME`| Name of the database to use within CouchDB       | `apisq_db`                |
| `APP_HOST`       | Host address for the FastAPI application to bind | `0.0.0.0`                 |
| `APP_PORT`       | Port for the FastAPI application to listen on    | `8000`                    |
| `LOG_LEVEL`      | Logging level for the application                | `INFO`                    |
| `PROJECT_NAME`   | Name of the project (used in API metadata)       | `"i2b-demo-python API"`   |
| `API_V1_STR`     | Base path prefix for API version 1               | `/api/v1`                 |

## Other Commands

Use `just --list` to see all available commands defined in the `justfile`.
