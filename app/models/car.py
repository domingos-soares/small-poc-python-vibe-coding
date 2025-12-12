from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


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

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
