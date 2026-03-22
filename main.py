from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

# ---------------- DATA ----------------
products = [
    {"id": 1, "name": "Kurta Set", "brand": "Biba", "category": "Ethnic", "price": 1500, "sizes_available": ["S","M","L"], "in_stock": True},
    {"id": 2, "name": "Saree", "brand": "Biba", "category": "Traditional", "price": 2500, "sizes_available": ["Free"], "in_stock": True},
    {"id": 3, "name": "Lehenga", "brand": "Biba", "category": "Bridal", "price": 5000, "sizes_available": ["M","L"], "in_stock": True},
    {"id": 4, "name": "Anarkali", "brand": "Biba", "category": "Ethnic", "price": 3000, "sizes_available": ["S","M"], "in_stock": False},
]

orders = []
wishlist = []
order_counter = 1

# ---------------- MODELS ----------------
class NewProduct(BaseModel):
    name: str = Field(min_length=2)
    brand: str = Field(min_length=2)
    category: str = Field(min_length=2)
    price: int = Field(gt=0)
    sizes_available: List[str]
    in_stock: bool = True

class OrderRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    product_id: int = Field(gt=0)
    size: str
    quantity: int = Field(gt=0)
    delivery_address: str = Field(min_length=10)

# ---------------- HELPERS ----------------
def find_product(pid):
    for p in products:
        if p["id"] == pid:
            return p
    return None

def calc_total(price, qty):
    return price * qty

# ---------------- BASIC ----------------
@app.get("/")
def home():
    return {"message": "Welcome to Fashion Store"}

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products),
        "in_stock_count": len([p for p in products if p["in_stock"]])
    }

@app.get("/products/summary")
def summary():
    return {
        "total_products": len(products),
        "in_stock": len([p for p in products if p["in_stock"]]),
        "out_of_stock": len([p for p in products if not p["in_stock"]]),
        "brands": list(set(p["brand"] for p in products)),
        "category_count": {
            c: len([p for p in products if p["category"] == c])
            for c in set(p["category"] for p in products)
        }
    }

@app.get("/orders")
def get_orders():
    return {
        "orders": orders,
        "total": len(orders),
        "total_revenue": sum(o["total"] for o in orders)
    }

# ---------------- Q11 CREATE PRODUCT ----------------
@app.post("/products", status_code=201)
def create_product(p: NewProduct):
    for prod in products:
        if prod["name"] == p.name and prod["brand"] == p.brand:
            raise HTTPException(400, "Duplicate product")

    new = p.dict()
    new["id"] = len(products) + 1
    products.append(new)
    return new

# ---------------- FILTER ----------------
@app.get("/products/filter")
def filter_products(category: str=None, brand: str=None, max_price: int=None, in_stock: bool=None):
    result = products

    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]
    if brand:
        result = [p for p in result if p["brand"].lower() == brand.lower()]
    if max_price:
        result = [p for p in result if p["price"] <= max_price]
    if in_stock is not None:
        result = [p for p in result if p["in_stock"] == in_stock]

    return {"total": len(result), "data": result}

# ---------------- Q16 SEARCH ----------------
@app.get("/products/search")
def search(keyword: str):
    result = [
        p for p in products
        if keyword.lower() in p["name"].lower()
        or keyword.lower() in p["brand"].lower()
        or keyword.lower() in p["category"].lower()
    ]

    if not result:
        return {"message": "No products found"}

    return {"results": result, "total_found": len(result)}

# ---------------- Q17 SORT ----------------
@app.get("/products/sort")
def sort_products(sort_by: str="price", order: str="asc"):
    if sort_by not in ["price","name","brand","category"]:
        raise HTTPException(400, "Invalid sort_by")

    if order not in ["asc","desc"]:
        raise HTTPException(400, "Invalid order")

    return {
        "data": sorted(products, key=lambda x: x[sort_by], reverse=(order=="desc"))
    }

# ---------------- Q18 PAGINATION ----------------
@app.get("/products/page")
def paginate(page:int=1, limit:int=3):
    start = (page-1)*limit
    total_pages = (len(products)+limit-1)//limit

    return {
        "page": page,
        "total_pages": total_pages,
        "data": products[start:start+limit]
    }

# ---------------- Q20 BROWSE ----------------
@app.get("/products/browse")
def browse(keyword:str=None, category:str=None, brand:str=None, in_stock:bool=None,
           max_price:int=None, sort_by:str="price", order:str="asc",
           page:int=1, limit:int=3):

    result = products

    # FILTER
    if category:
        result = [p for p in result if p["category"].lower()==category.lower()]
    if brand:
        result = [p for p in result if p["brand"].lower()==brand.lower()]
    if in_stock is not None:
        result = [p for p in result if p["in_stock"]==in_stock]
    if max_price:
        result = [p for p in result if p["price"]<=max_price]

    # SEARCH
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
            or keyword.lower() in p["brand"].lower()
            or keyword.lower() in p["category"].lower()
        ]

    # SORT
    result = sorted(result, key=lambda x: x[sort_by], reverse=(order=="desc"))

    # PAGINATION
    total = len(result)
    start = (page-1)*limit

    return {
        "total": total,
        "page": page,
        "data": result[start:start+limit]
    }

# ---------------- Q19 ORDER SEARCH/SORT/PAGE ----------------
@app.get("/orders/search")
def order_search(customer_name: str):
    return {"results": [o for o in orders if o["customer"] == customer_name]}

@app.get("/orders/sort")
def order_sort(sort_by: str="total"):
    return {"data": sorted(orders, key=lambda x: x[sort_by])}

@app.get("/orders/page")
def order_page(page:int=1, limit:int=2):
    start = (page-1)*limit
    return {"data": orders[start:start+limit]}

# ---------------- Q14 CREATE ORDER ----------------
@app.post("/orders")
def create_order(req: OrderRequest):
    global order_counter

    p = find_product(req.product_id)
    if not p:
        raise HTTPException(404, "Product not found")

    if req.size not in p["sizes_available"]:
        raise HTTPException(400, "Invalid size")

    total = calc_total(p["price"], req.quantity)

    order = {
        "id": order_counter,
        "customer": req.customer_name,
        "product_id": req.product_id,
        "quantity": req.quantity,
        "total": total
    }

    orders.append(order)
    order_counter += 1

    return order

# ---------------- Q14 WISHLIST ----------------
@app.post("/wishlist/add")
def add_wishlist(customer_name: str, product_id: int, size: str):

    p = find_product(product_id)
    if not p:
        raise HTTPException(404, "Product not found")

    if size not in p["sizes_available"]:
        raise HTTPException(400, "Invalid size")

    for w in wishlist:
        if w["customer"]==customer_name and w["product_id"]==product_id and w["size"]==size:
            raise HTTPException(400, "Duplicate wishlist entry")

    wishlist.append({
        "customer": customer_name,
        "product_id": product_id,
        "size": size
    })

    return {"message": "Added to wishlist"}

@app.get("/wishlist")
def get_wishlist():
    total = sum(find_product(w["product_id"])["price"] for w in wishlist)
    return {"items": wishlist, "total_value": total}

# ---------------- Q15 REMOVE + ORDER ALL ----------------
@app.delete("/wishlist/remove")
def remove_wishlist(customer_name: str, product_id: int):
    for w in wishlist:
        if w["customer"]==customer_name and w["product_id"]==product_id:
            wishlist.remove(w)
            return {"message": "Removed"}
    raise HTTPException(404, "Not found")

@app.post("/wishlist/order-all", status_code=201)
def order_all(customer_name: str, delivery_address: str):
    global order_counter

    user_items = [w for w in wishlist if w["customer"]==customer_name]
    if not user_items:
        raise HTTPException(400, "Wishlist empty")

    created_orders = []
    grand_total = 0

    for w in user_items:
        p = find_product(w["product_id"])

        order = {
            "id": order_counter,
            "customer": customer_name,
            "product_id": w["product_id"],
            "quantity": 1,
            "total": p["price"]
        }

        orders.append(order)
        created_orders.append(order)
        grand_total += p["price"]
        order_counter += 1

    # clear wishlist
    wishlist[:] = [w for w in wishlist if w["customer"] != customer_name]

    return {
        "orders": created_orders,
        "grand_total": grand_total
    }

# ---------------- VARIABLE ROUTES ----------------
@app.get("/products/{product_id}")
def get_product(product_id: int):
    p = find_product(product_id)
    if not p:
        raise HTTPException(404, "Product not found")
    return p

@app.put("/products/{product_id}")
def update_product(product_id: int, price: int=None, in_stock: bool=None):
    p = find_product(product_id)
    if not p:
        raise HTTPException(404, "Not found")

    if price is not None:
        p["price"] = price
    if in_stock is not None:
        p["in_stock"] = in_stock

    return p

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    p = find_product(product_id)
    if not p:
        raise HTTPException(404, "Not found")

    for o in orders:
        if o["product_id"] == product_id:
            raise HTTPException(400, "Cannot delete product with orders")

    products.remove(p)
    return {"message": "Deleted"}