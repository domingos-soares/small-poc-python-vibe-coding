from typing import Dict, List, Optional
from datetime import datetime
import uuid

from app.models.car import Car, CarCreate, CarUpdate, CarPartialUpdate


class CarService:
    def __init__(self):
        self._cars_db: Dict[str, Car] = {}
    
    def _generate_car_id(self) -> str:
        return str(uuid.uuid4())
    
    def _get_current_timestamp(self) -> datetime:
        return datetime.utcnow()
    
    def get_all_cars(self) -> List[Car]:
        """Get all cars"""
        return list(self._cars_db.values())
    
    def get_car_by_id(self, car_id: str) -> Optional[Car]:
        """Get a specific car by ID"""
        return self._cars_db.get(car_id)
    
    def create_car(self, car_data: CarCreate) -> Car:
        """Create a new car"""
        car_id = self._generate_car_id()
        timestamp = self._get_current_timestamp()
        
        new_car = Car(
            id=car_id,
            created_at=timestamp,
            updated_at=timestamp,
            **car_data.model_dump()
        )
        
        self._cars_db[car_id] = new_car
        return new_car
    
    def update_car(self, car_id: str, car_data: CarUpdate) -> Optional[Car]:
        """Update a car completely (replace all fields)"""
        existing_car = self._cars_db.get(car_id)
        if not existing_car:
            return None
        
        updated_car = Car(
            id=car_id,
            created_at=existing_car.created_at,
            updated_at=self._get_current_timestamp(),
            **car_data.model_dump()
        )
        
        self._cars_db[car_id] = updated_car
        return updated_car
    
    def partial_update_car(self, car_id: str, car_data: CarPartialUpdate) -> Optional[Car]:
        """Partially update a car (update only provided fields)"""
        existing_car = self._cars_db.get(car_id)
        if not existing_car:
            return None
        
        update_data = car_data.model_dump(exclude_unset=True)
        
        if not update_data:
            raise ValueError("No fields provided for update")
        
        updated_car = Car(
            id=car_id,
            created_at=existing_car.created_at,
            updated_at=self._get_current_timestamp(),
            make=update_data.get("make", existing_car.make),
            model=update_data.get("model", existing_car.model),
            year=update_data.get("year", existing_car.year),
            color=update_data.get("color", existing_car.color),
            price=update_data.get("price", existing_car.price)
        )
        
        self._cars_db[car_id] = updated_car
        return updated_car
    
    def delete_car(self, car_id: str) -> bool:
        """Delete a car"""
        if car_id in self._cars_db:
            del self._cars_db[car_id]
            return True
        return False


# Global instance
car_service = CarService()
