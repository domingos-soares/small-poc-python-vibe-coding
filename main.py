from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import uuid
import uvicorn

app = FastAPI(title="Cars REST API", version="1.0.0")

# Pydantic models
class CarBase(BaseModel):
    make: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1900, le=2030)
    color: str = Field(..., min_length=1, max_length=30)
    price: float = Field(..., gt=0)

class CarCreate(CarBase):
    pass

class CarUpdate(CarBase):
    pass

class CarPartialUpdate(BaseModel):
    make: Optional[str] = Field(None, min_length=1, max_length=50)
    model: Optional[str] = Field(None, min_length=1, max_length=50)
    year: Optional[int] = Field(None, ge=1900, le=2030)
    color: Optional[str] = Field(None, min_length=1, max_length=30)
    price: Optional[float] = Field(None, gt=0)

class Car(CarBase):
    id: str
    created_at: datetime
    updated_at: datetime

# In-memory storage
cars_db: Dict[str, Car] = {}

def generate_car_id() -> str:
    return str(uuid.uuid4())

def get_current_timestamp() -> datetime:
    return datetime.utcnow()

# Routes
@app.get("/")
async def root():
    return {"message": "Cars REST API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": get_current_timestamp().isoformat(),
        "service": "Cars REST API"
    }

@app.get("/cars")
async def get_cars():
    """GET /cars - Get all cars"""
    return list(cars_db.values())

@app.get("/cars/{car_id}")
async def get_car(car_id: str):
    """GET /cars/{id} - Get a specific car by ID"""
    if car_id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")
    return cars_db[car_id]

@app.post("/cars", status_code=201)
async def create_car(car_data: CarCreate):
    """POST /cars - Create a new car"""
    car_id = generate_car_id()
    timestamp = get_current_timestamp()
    
    new_car = Car(
        id=car_id,
        created_at=timestamp,
        updated_at=timestamp,
        **car_data.model_dump()
    )
    
    cars_db[car_id] = new_car
    return new_car

@app.put("/cars/{car_id}")
async def update_car(car_id: str, car_data: CarUpdate):
    """PUT /cars/{id} - Update a car completely"""
    if car_id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")
    
    existing_car = cars_db[car_id]
    updated_car = Car(
        id=car_id,
        created_at=existing_car.created_at,
        updated_at=get_current_timestamp(),
        **car_data.model_dump()
    )
    
    cars_db[car_id] = updated_car
    return updated_car

@app.patch("/cars/{car_id}")
async def partial_update_car(car_id: str, car_data: CarPartialUpdate):
    """PATCH /cars/{id} - Partially update a car"""
    if car_id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")
    
    existing_car = cars_db[car_id]
    update_data = car_data.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    updated_car = Car(
        id=car_id,
        created_at=existing_car.created_at,
        updated_at=get_current_timestamp(),
        make=update_data.get("make", existing_car.make),
        model=update_data.get("model", existing_car.model),
        year=update_data.get("year", existing_car.year),
        color=update_data.get("color", existing_car.color),
        price=update_data.get("price", existing_car.price)
    )
    
    cars_db[car_id] = updated_car
    return updated_car

@app.delete("/cars/{car_id}", status_code=204)
async def delete_car(car_id: str):
    """DELETE /cars/{id} - Delete a car"""
    if car_id not in cars_db:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")
    
    del cars_db[car_id]
    return None

if __name__ == "__main__":
    print("🚀 Starting Cars REST API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
