from fastapi import FastAPI

import fastapi
print(f"Путь к FastAPI: {fastapi.__file__}")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """
    this is description
    """
    return {"item_id": item_id, "q": q}

@app.get("/openapi")
def openapi():
    return app.openapi()
