# main.py

from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from auth.router import router
from users.router import user_router


app = FastAPI(
	title = "My API",
	swagger_ui_oauth2_redirect_url = "/oauth2-redirect"
)
app.include_router(router)
app.include_router(user_router)


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