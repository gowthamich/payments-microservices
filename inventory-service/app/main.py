from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Inventory Service")

inventory = {
    5001: {"product_id": 5001, "name": "Laptop", "price": 750.0, "stock": 10},
    5002: {"product_id": 5002, "name": "Mobile", "price": 500.0, "stock": 20},
}

class ReserveRequest(BaseModel):
    quantity: int

@app.get("/health")
def health():
    return {"status": "UP", "service": "inventory-service"}

@app.get("/inventory/{product_id}")
def get_inventory(product_id: int):
    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    return inventory[product_id]

@app.post("/inventory/{product_id}/reserve")
def reserve_product(product_id: int, request: ReserveRequest):
    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    if request.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")
    if inventory[product_id]["stock"] < request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    inventory[product_id]["stock"] -= request.quantity
    return {
        "message": "Product reserved",
        "product_id": product_id,
        "quantity": request.quantity,
        "remaining_stock": inventory[product_id]["stock"],
    }
