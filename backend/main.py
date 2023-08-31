import uvicorn
from app.endpoints.router import router
from fastapi import FastAPI


def create_app():
    app = FastAPI()
    app.include_router(router)

    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", workers=1, factory=True)
