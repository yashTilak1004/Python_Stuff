from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

class Obj(BaseModel):
    id:int
    name:str
    role:str=None

def read_file():
    with open("data.json","r") as f:
        return json.load(f)

def write(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

#get item based on an id
@app.get("/obj")
def read_items():
    data = read_file()
    return data["Characters"]

@app.post("/new")
def create(item:Obj):
    data = read_file()
    data["Characters"].append(item.dict())
    write(data)
    return item

@app.delete("/delete")
def delete(id:int):
    data = read_file()
    new_data = [item for item in data["Characters"] if item["id"] != id]
    if len(new_data) == len(data["Characters"]):
        raise HTTPException(status_code=404, detail="Item not found.")#raise an error when id doesn't match
    data["Characters"] = new_data
    write(data)
    return new_data