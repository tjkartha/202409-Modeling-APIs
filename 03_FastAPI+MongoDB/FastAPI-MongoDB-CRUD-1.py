# %% [markdown]
# # FastAPI and MongoDB

# %%
# !pip install fastapi
# !pip install uvicorn
# !pip install motor

# %% [markdown]
# ## Let's make a setup

# %%
# Importing libraries
from fastapi import FastAPI, HTTPException          # FastAPI utilities
from motor.motor_asyncio import AsyncIOMotorClient  # Asynchronous motor client
from pydantic import BaseModel                      # pydantic for data validation 
from bson import ObjectId                           # bson is Binary JSON, used for some JSON management
from typing import List                             # 

# Setting up a FastAPI instance
app = FastAPI()
# MongoDB connection
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.fastapi_db

# Use the collection 
collection = db.users

# %%
# Let's define a pydantic model
class User(BaseModel):
    name: str
    email: str

class UserInDB(User):
    id: str

# %%
# A convertor for BSON to JSON
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }

# %% [markdown]
# Create User

# %%
@app.post("/users/", response_model=UserInDB)
async def create_user(user: User):
    user_dict = user.dict()
    new_user = await collection.insert_one(user_dict)
    created_user = await collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)

# %% [markdown]
# Read Users

# %%
@app.get("/users/", response_model=List[UserInDB])
async def get_users():
    users = []
    async for user in collection.find():
        users.append(user_helper(user))
    return users

# %% [markdown]
# Read single user

# %%
@app.get("/users/{user_id}", response_model=UserInDB)
async def get_user(user_id: str):
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)

# %% [markdown]
# Update User

# %%
@app.put("/users/{user_id}", response_model=UserInDB)
async def update_user(user_id: str, user: User):
    await collection.update_one({"_id": ObjectId(user_id)}, {"$set": user.dict()})
    updated_user = await collection.find_one({"_id": ObjectId(user_id)})
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(updated_user)

# %% [markdown]
# Delete User

# %%
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    delete_result = await collection.delete_one({"_id": ObjectId(user_id)})
    if delete_result.deleted_count == 1:
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

# %%



