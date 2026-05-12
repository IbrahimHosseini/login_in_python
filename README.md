# login_in_python

A small FastAPI authentication example that issues JWT access and refresh tokens.

The app currently uses an in-memory demo user store and an in-memory refresh-token set. It is useful for learning or prototyping the auth flow, but it is not production-ready without replacing those stores with a database-backed implementation.

## Features

- Login with email and password
- Password hashing and verification with `bcrypt`
- JWT access tokens and refresh tokens
- Refresh-token rotation
- Logout by invalidating the provided refresh token
- Protected `/auth/me` endpoint using bearer-token authentication

## Project Structure

```text
.
├── main.py
├── config.py
└── auth
    ├── dependencies.py
    ├── router.py
    ├── schemas.py
    └── service.py
```

## Requirements

This repo does not currently include a dependency manifest. The source imports these packages:

- `fastapi`
- `uvicorn`
- `python-jose`
- `bcrypt`
- `pydantic-settings`

Install them manually:

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn python-jose bcrypt pydantic-settings
```

## Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-this-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Only `SECRET_KEY` is required because the other values have defaults in `config.py`.

## Run

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Demo Credentials

The current demo user is defined in `auth/router.py`:

```text
email: user@test.com
password: testpass123
```

## API Endpoints

### Login

```http
POST /auth/login?email=user@test.com&password=testpass123
```

Returns:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

### Refresh Token

```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "..."
}
```

Refresh tokens are rotated. After a successful refresh, the old refresh token is removed and a new one is returned.

### Logout

```http
POST /auth/logout
Content-Type: application/json

{
  "refresh_token": "..."
}
```

Returns:

```json
{
  "message": "Logged out"
}
```

### Current User

```http
GET /auth/me
Authorization: Bearer <access_token>
```

Returns:

```json
{
  "user_id": "1"
}
```

## Notes

- Refresh tokens are stored in process memory, so they are lost when the server restarts.
- The demo user store is hard-coded and should be replaced with a database.
- `verify_token` raises `ValueError` for invalid JWTs; route-level error handling can be improved if this becomes more than a learning project.
