from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")    
def read_item(item_id):
    return {"item_id": item_id}

# After running the code,
# We must try going to http://127.0.0.1:8000/items/foo 
# or even http://127.0.0.1:8000/items/gold