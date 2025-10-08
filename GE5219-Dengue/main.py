#!/usr/bin/env python3

# Minimal FastAPI application bootstrap for the dengue dashboard.

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Dict

APP = FastAPI(title="GE5219 Real-Time Dengue Map")

static_root = Path(__file__).parent / "visualization" / "static"
APP.mount("/static", StaticFiles(directory=static_root), name="static")

@APP.get("/health")
async def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}

@APP.get("/")
async def index() -> Dict[str, str]:
    return {"message": "Serve visualization from /static/templates/index.html"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(APP, host="0.0.0.0", port=8000, reload=True)
