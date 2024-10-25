# Messaging API

A FastAPI-based service that manages users and messages with PostgreSQL as the database. The API provides endpoints for user and message CRUD operations

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features
- **User Management**: Create, update, soft delete, and retrieve users by email.
- **Messaging Service**: Create, receive, and soft delete messages.
- **Domain-Driven Design (DDD)**: Code is organized based on DDD principles for better scalability and maintenance.

## Technologies Used
- **FastAPI**: Web framework for building APIs.
- **SQLModel**: Pydantic models + SQLAlchemy ORM for PostgreSQL.
- **PostgreSQL**: Database to store user and message data.
- **SQLAlchemy**: ORM used for database operations.
- **pytest**: Testing framework.
- **pre-commit**: Code quality and style checks.

## Setup
### Docker

1. Clone the repository
    ```bash
    git clone git@github.com:timkatala/assignment.git
    ```
2. Configure the environment variables (see `.env_example`)
    ```bash
    cp .env_example .env
    ```
3. Run the docker compose
    ```bash
    docker compose up
    ```

## Usage
**API Documentation** : Visit http://localhost:8000/docs for interactive API documentation.

## Testing
1. **Run Tests**
    ```bash
    python -m pytest
    ```
2. **Pre-commit Hooks** Run all pre-commit hooks to check code formatting and quality
    ```bash
    pre-commit run --all-files
    ```