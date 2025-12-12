from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
import uuid

app = FastAPI(
    title="Cars REST API",
    description="A REST service to manage cars with full CRUD operations",
    version="1.0.0"
)

# Pydantic models
class CarBase(BaseModel):
    make: str = Field(..., min_length=1, max_length=50, description="Car manufacturer")
    model: str = Field(..., min_length=1, max_length=50, description="Car model")
    year: int = Field(..., ge=1900, le=2030, description="Manufacturing year")
    color: str = Field(..., min_length=1, max_length=30, description="Car color")
    price: float = Field(..., gt=0, description="Car price in USD")

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
    id: str = Field(..., description="Unique car identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# In-memory storage (replace with database in production)
cars_db: Dict[str, Car] = {}

# Helper functions
def generate_car_id() -> str:
    return str(uuid.uuid4())

def get_current_timestamp() -> datetime:
    return datetime.utcnow()

# Routes
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Cars REST API", "version": "1.0.0"}

@app.get("/cars", response_model=List[Car], tags=["Cars"])
async def get_cars():
    """Get all cars"""
    return list(cars_db.values())

@app.get("/cars/{car_id}", response_model=Car, tags=["Cars"])
async def get_car(car_id: str):
    """Get a specific car by ID"""
    if car_id not in cars_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    return cars_db[car_id]

@app.post("/cars", response_model=Car, status_code=status.HTTP_201_CREATED, tags=["Cars"])
async def create_car(car_data: CarCreate):
    """Create a new car"""
    car_id = generate_car_id()
    timestamp = get_current_timestamp()
    
    new_car = Car(
        id=car_id,
        created_at=timestamp,
        updated_at=timestamp,
        **car_data.dict()
    )
    
    cars_db[car_id] = new_car
    return new_car

@app.put("/cars/{car_id}", response_model=Car, tags=["Cars"])
async def update_car(car_id: str, car_data: CarUpdate):
    """Update a car completely (replace all fields)"""
    if car_id not in cars_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    
    existing_car = cars_db[car_id]
    updated_car = Car(
        id=car_id,
        created_at=existing_car.created_at,
        updated_at=get_current_timestamp(),
        **car_data.dict()
    )
    
    cars_db[car_id] = updated_car
    return updated_car

@app.patch("/cars/{car_id}", response_model=Car, tags=["Cars"])
async def partial_update_car(car_id: str, car_data: CarPartialUpdate):
    """Partially update a car (update only provided fields)"""
    if car_id not in cars_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    
    existing_car = cars_db[car_id]
    update_data = car_data.dict(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    
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

@app.delete("/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Cars"])
async def delete_car(car_id: str):
    """Delete a car"""
    if car_id not in cars_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    
    del cars_db[car_id]
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
