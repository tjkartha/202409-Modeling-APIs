from fastapi import FastAPI
import pymongo

app = FastAPI()

# Connect to the MongoDB database
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['test_db']
col = db['test_col']

@app.get("/")
async def read_items():
    # Retrieve all documents from the collection
    docs = col.find()
    return docs

@app.post("/")
async def create_item(item: dict):
    # Insert a new document into the collection
    result = col.insert_one(item)
    return {"result": result}

@app.put("/{id}")
async def update_item(id: int, item: dict):
    # Update an existing document in the collection
    result = col.update_one({"_id": id}, {"$set": item})
    return {"result": result}

@app.delete("/{id}")
async def delete_item(id: int):
    # Delete a document from the collection
    result = col.delete_one({"_id": id})
    return {"result": result}
