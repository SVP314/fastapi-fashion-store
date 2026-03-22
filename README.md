# FastAPI Fashion Store Backend

## Project Description
This project is a backend application developed using FastAPI as part of internship training. It simulates a Fashion Store system and demonstrates real-world API development concepts.

---

## Features Implemented

### GET APIs
- Home route
- Get all products
- Get product by ID
- Product count/summary

### POST APIs with Validation
- Implemented using Pydantic models
- Input validation and error handling

### CRUD Operations
- Create product (POST)
- Read product (GET)
- Update product (PUT)
- Delete product (DELETE)

### Helper Functions
- Search functionality
- Filtering logic

### Multi-Step Workflow
- Cart → Order → Checkout

### Advanced APIs
- Search by keyword
- Sorting
- Pagination
- Combined browsing endpoint

---

## Tech Stack
- Python
- FastAPI
- Uvicorn
- Pydantic

---

## How to Run

Install dependencies:
pip install -r requirements.txt

Run server:
uvicorn main:app --reload

Open Swagger:
http://127.0.0.1:8000/docs

---

## Project Structure
fashion_api/
│── main.py
│── requirements.txt
│── README.md
└── screenshots/
