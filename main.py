from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Process the image data, for example, you can save it to a file
        print(f"test")

# In-memory database (for demonstration purposes)
items = []

# Pydantic model for item data
class Item(BaseModel):
    name: str
    description: str

@app.get("/", tags=["Root"])
async def hello():
    return{"hello":"Your deploy is success"}

# Create an item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

# Get an item
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# Update an item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    items[item_id] = item
    return item

# Delete an item
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = items.pop(item_id)
    return deleted_item
