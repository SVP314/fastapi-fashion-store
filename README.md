# 🛍️ Fashion Store API

🚀 FastAPI-based Fashion Store API with product management, cart workflow, filtering, sorting, and pagination. Built as a complete backend project.

---

## 📌 Project Overview
A fully functional FastAPI-based Fashion Store System built as a final project. This API allows users to browse products, manage a cart, place orders, and handle workflows with advanced features.

---

## 🚀 Features

### 👗 Products Management
- View all products  
- Get product by ID  
- Add new products  
- Update product details  
- Delete products (with validation)  

---

### 🛒 Cart System
- Add items to cart  
- Merge quantities automatically  
- Remove items  
- View cart  
- Checkout system  

---

### 📦 Orders System
- Create orders  
- View all orders  

---

### 🔍 Advanced Features
- Search products by keyword  
- Filter products (category, price, etc.)  
- Sort products (price, name, category)  
- Pagination for products  
- Combined browsing endpoint  

---

### ⚙️ Helper Functions
- find_product() for product lookup  
- calculate_total() for cart/order  

---

## 🧪 API Endpoints Overview

### 🟢 Basic
GET / → Welcome message  
GET /products  
GET /products/{id}  
GET /products/count  

---

### 🔵 Products Advanced
GET /products/filter  
GET /products/search  
GET /products/sort  
GET /products/page  
GET /products/browse  

---

### 🟠 Cart
POST /cart  
GET /cart  
DELETE /cart/{id}  
POST /cart/checkout  

---

### 🟣 Orders
POST /orders  
GET /orders  

---

## ⚙️ Tech Stack
⚡ FastAPI  
🐍 Python  
📦 Pydantic (Data Validation)  
🚀 Uvicorn (ASGI Server)  

---

## ▶️ How to Run the Project

### 1. Clone Repository
git clone https://github.com/SVP314/fastapi-fashion-store.git  
cd fastapi-fashion-store  

### 2. Install Dependencies
pip install -r requirements.txt  

### 3. Run Server
uvicorn main:app --reload  

### 4. Open Swagger UI
http://127.0.0.1:8000/docs  

---

## 📸 Screenshots
All API endpoints are tested using Swagger UI. Screenshots are available in the /screenshots folder.

---

## 💡 Key Highlights
- Clean and modular code structure  
- Proper use of Pydantic validation  
- Real-world cart & checkout workflow  
- Fully implemented search, sort, pagination  
- Error handling with proper status codes  

---

## 🧠 Learning Outcomes
- Built REST APIs using FastAPI  
- Implemented CRUD operations  
- Designed multi-step workflows  
- Applied filtering, sorting, pagination  

---

## 👨‍💻 Author
Swathi P V 
