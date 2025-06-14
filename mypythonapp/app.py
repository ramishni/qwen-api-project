from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str = "World"

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI!"}

@app.post("/call")
async def call_function(item: Item):
    return {"message": f"Hello {item.name} from FastAPI!"}
