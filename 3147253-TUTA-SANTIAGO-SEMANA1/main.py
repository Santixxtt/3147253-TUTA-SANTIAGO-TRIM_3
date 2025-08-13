from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def my_first_api() -> dict:
    return {"message": "My first API"}