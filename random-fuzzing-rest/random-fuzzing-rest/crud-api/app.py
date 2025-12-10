from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

DB = {}

class Item(BaseModel):
    name: str
    price: float
    stock: int

@app.post("/items")
def create_item(item: Item):
    new_id = random.randint(1, 999999)
    DB[new_id] = item
    return {"id": new_id, "item": item}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    return DB[item_id]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    DB[item_id] = item
    return {"updated": item_id}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    del DB[item_id]
    return {"deleted": item_id}
