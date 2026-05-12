# main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from auth.router import router


app = FastAPI()
app.include_router(router)


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