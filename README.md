# Cars REST API

A FastAPI-based REST service for managing cars with full CRUD operations.

## Features

- **GET /cars** - List all cars
- **GET /cars/{id}** - Get a specific car by ID
- **POST /cars** - Create a new car
- **PUT /cars/{id}** - Update a car completely
- **PATCH /cars/{id}** - Partially update a car
- **DELETE /cars/{id}** - Delete a car

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## Car Model

Each car has the following properties:
- `id` (string): Unique identifier (auto-generated)
- `make` (string): Car manufacturer (1-50 characters)
- `model` (string): Car model (1-50 characters)
- `year` (integer): Manufacturing year (1900-2030)
- `color` (string): Car color (1-30 characters)
- `price` (float): Car price in USD (must be positive)
- `created_at` (datetime): Creation timestamp (auto-generated)
- `updated_at` (datetime): Last update timestamp (auto-updated)

## API Endpoints

### GET /cars
Returns a list of all cars.

**Response**: `200 OK`
```json
[
  {
    "id": "uuid-string",
    "make": "Toyota",
    "model": "Camry",
    "year": 2023,
    "color": "Blue",
    "price": 25000.0,
    "created_at": "2023-12-11T14:37:00Z",
    "updated_at": "2023-12-11T14:37:00Z"
  }
]
```

### GET /cars/{id}
Returns a specific car by ID.

**Response**: `200 OK` or `404 Not Found`

### POST /cars
Creates a new car.

**Request Body**:
```json
{
  "make": "Toyota",
  "model": "Camry",
  "year": 2023,
  "color": "Blue",
  "price": 25000.0
}
```

**Response**: `201 Created`

### PUT /cars/{id}
Updates a car completely (all fields required).

**Request Body**: Same as POST
**Response**: `200 OK` or `404 Not Found`

### PATCH /cars/{id}
Partially updates a car (only provided fields are updated).

**Request Body** (all fields optional):
```json
{
  "color": "Red",
  "price": 26000.0
}
```

**Response**: `200 OK` or `404 Not Found`

### DELETE /cars/{id}
Deletes a car.

**Response**: `204 No Content` or `404 Not Found`

## Example Usage

### Create a car
```bash
curl -X POST "http://localhost:8000/cars" \
  -H "Content-Type: application/json" \
  -d '{
    "make": "Honda",
    "model": "Civic",
    "year": 2022,
    "color": "White",
    "price": 22000.0
  }'
```

### Get all cars
```bash
curl "http://localhost:8000/cars"
```

### Update car color
```bash
curl -X PATCH "http://localhost:8000/cars/{car_id}" \
  -H "Content-Type: application/json" \
  -d '{"color": "Black"}'
```

### Delete a car
```bash
curl -X DELETE "http://localhost:8000/cars/{car_id}"
```

## Data Storage

This implementation uses in-memory storage for simplicity. In a production environment, you would typically integrate with a database like PostgreSQL, MySQL, or MongoDB.
