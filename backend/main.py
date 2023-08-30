from fastapi import FastAPI
import uvicorn


app = FastAPI()


def create_app():
    return app


if __name__ == "__main__":
    uvicorn.run(app, workers=1, factory=True)
