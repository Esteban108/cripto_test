import uvicorn
from fastapi import FastAPI

from .routers import routers

app = FastAPI(title="Cripto")

for r in routers:
    app.include_router(r)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
