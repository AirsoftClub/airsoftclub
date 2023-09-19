import uvicorn
from app.endpoints.router import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


def create_app():
    app = FastAPI()

    app.include_router(router)

    app.mount("/static", app=StaticFiles(directory="static"), name="static")

    origins = [
        "http://localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", workers=1, factory=True)
