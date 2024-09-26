# We will try with an integer as well

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Try opening http://127.0.0.1:8000/items/3 or so in the browser
# It should be an integer, and not a string

# We should also try going to http://127.0.0.1:8000/items/foo
# to see a nice error message. 

# Similar errors would be obtained with http://127.0.0.1:8000/items/5.6 as well
# since 5.6 is float and not int.

# Pydantic is responsible for doing this data validation.
