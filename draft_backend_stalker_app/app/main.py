from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from api.v1.api import api_router

import uvicorn
import logging
import sys

# @asynccontextmanager
# async def lifespan(app: FastAPI):
	

app = FastAPI(title="StalkBackend")

app.include_router(api_router, prefix="/api/v1")

@app.get("/", response_class=RedirectResponse)
async def redirect_docs():
	return "/docs"

if __name__ == "__main__":
	try:
		uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")
	except KeyboardInterrupt as exc:
		logging.info(f"Keyboard interrupt")
	except Exception as exc:
		logging.info(f"Error: {exc}")
		sys.exit(0)