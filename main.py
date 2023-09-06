from fastapi import FastAPI
from pydantic import BaseModel
from nlp.process import process

class Item(BaseModel):
    data: list

app = FastAPI()

@app.get("/")
async def root():
    return {"status":"ready"}

@app.post("/get_analysis/")
async def get_analysis(data: Item):
    result = process(data.data)
    return result