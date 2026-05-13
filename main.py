# main.py

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from auth.router import router
from users.router import user_router

app = FastAPI()
app.include_router(router)
app.include_router(user_router)

def custom_openapi():
	if app.openapi_schema:
		return app.openapi_schema
	openapi_schema = get_openapi(
		title = "My API",
		version = "0.1.0",
		routes = app.routes
	)
	app.openapi_schema = openapi_schema
	return app.openapi_schema

app.openapi = custom_openapi

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
	return JSONResponse(
		status_code = 500,
		content = {"detail": "Internal server error"}
	)

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: Exception):
	return JSONResponse(
		status_code = 401,
		content = {"detail": "Invalid Token"}
	)