from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.car import Car, CarCreate, CarUpdate, CarPartialUpdate
from app.services.car_service import car_service

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.get("", response_model=List[Car])
async def get_cars():
    """Get all cars"""
    return car_service.get_all_cars()


@router.get("/{car_id}", response_model=Car)
async def get_car(car_id: str):
    """Get a specific car by ID"""
    car = car_service.get_car_by_id(car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    return car


@router.post("", response_model=Car, status_code=status.HTTP_201_CREATED)
async def create_car(car_data: CarCreate):
    """Create a new car"""
    return car_service.create_car(car_data)


@router.put("/{car_id}", response_model=Car)
async def update_car(car_id: str, car_data: CarUpdate):
    """Update a car completely (replace all fields)"""
    updated_car = car_service.update_car(car_id, car_data)
    if not updated_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    return updated_car


@router.patch("/{car_id}", response_model=Car)
async def partial_update_car(car_id: str, car_data: CarPartialUpdate):
    """Partially update a car (update only provided fields)"""
    try:
        updated_car = car_service.partial_update_car(car_id, car_data)
        if not updated_car:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Car with id {car_id} not found"
            )
        return updated_car
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: str):
    """Delete a car"""
    deleted = car_service.delete_car(car_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    return None
