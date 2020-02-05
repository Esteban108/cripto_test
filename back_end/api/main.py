import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routers import routers

app = FastAPI(title="Cripto")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in routers:
    app.include_router(r)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
