import uvicorn
from app.endpoints.router import router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def create_app():
    app = FastAPI()

    app.include_router(router)

    app.mount("/static", app=StaticFiles(directory="static"), name="static")

    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", workers=1, factory=True)
