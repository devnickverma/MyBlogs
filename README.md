# FastAPI Blog Backend

A professional, modular, and fully tested backend for a blog/social application built with **FastAPI**, **SQLAlchemy**, and **SQLite**.

## Features

- **Users**: Registration, Authentication (JWT), Profile retrieval.
- **Posts**: Create posts (Markdown supported), List posts (Newest first), Read post details.
- **Comments**: Add comments to posts, List comments for a post.
- **Likes**: Like and Unlike posts, Duplicate like prevention.
- **Authentication**: Secure OAuth2 Password Bearer flow (HS256 JWTs).
- **Architecture**:
    - **Modular**: Routers, CRUD, Models, Schemas, Dependencies.
    - **Reliable**: Pydantic V2 validation, domain-specific exception handling.
    - **Testable**: Isolated in-memory database strategy for integration tests.

## Architecture

```
fastapi-backend/
├── app/
│   ├── core/           # Config, Database, Security
│   ├── crud/           # Database operations (Business Logic)
│   ├── models/         # SQLAlchemy ORM models
│   ├── routers/        # API Endpoints
│   ├── schemas/        # Pydantic Schemas (V2)
│   ├── dependencies.py # Dependency Injection (get_db, get_current_user)
│   ├── exceptions.py   # Domain Exceptions & Handlers
│   └── main.py         # Application Entrypoint
├── tests/              # Pytest Integration Tests
├── .env.example        # Environment variables template
├── pytest.ini          # Test configuration
└── requirements.txt    # Dependencies
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd fastapi-backend
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**:
    Copy `.env.example` to `.env` (optional, defaults are set in `config.py`).
    ```bash
    cp .env.example .env
    ```

### Running the Application

Start the development server:

uvicorn app.main:app --reload
```

### Deployment

To deploy for production (e.g., Render, Fly.io):

1.  **Set Environment Variables**:
    - `SECRET_KEY`: Generate a strong random string.
    - `PORT`: (Optional) Provided by your platform.

2.  **Start Command**:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
    ```
    *Note: The application also supports running as a script: `python app/main.py` which respects the `PORT` env var.*

The API will be available at `http://127.0.0.1:8000`.
Access the interactive documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Authentication

1.  **Sign Up**: `POST /users/`
2.  **Login**: `POST /token` with `username` (email) and `password`.
    - Response: `{ "access_token": "...", "token_type": "bearer" }`
3.  **Use Token**: Click "Authorize" in Swagger UI or send header `Authorization: Bearer <token>` for protected endpoints.

Protected Routes:
- `POST /posts/`
- `POST /comments`
- `POST /likes/`
- `DELETE /likes/`

## Testing

This project uses **pytest** with an **in-memory SQLite database** for completely isolated and fast integration tests.

Run all tests:

```bash
pytest
```
(No warnings expected)

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite, SQLAlchemy
- **Validation**: Pydantic V2
- **Auth**: OAuth2, python-jose, passlib
- **Testing**: Pytest, Httpx
