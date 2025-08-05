from fastapi import FastAPI, APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import json
from passlib.context import CryptContext
from jose import JWTError, jwt
from passlib.hash import bcrypt

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# WebSocket connection manager for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.admin_connections: List[WebSocket] = []
        self.delivery_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, connection_type: str = "client"):
        await websocket.accept()
        if connection_type == "admin":
            self.admin_connections.append(websocket)
        elif connection_type == "delivery":
            self.delivery_connections.append(websocket)
        else:
            self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket, connection_type: str = "client"):
        if connection_type == "admin" and websocket in self.admin_connections:
            self.admin_connections.remove(websocket)
        elif connection_type == "delivery" and websocket in self.delivery_connections:
            self.delivery_connections.remove(websocket)
        elif websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_admins(self, message: dict):
        for connection in self.admin_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                self.admin_connections.remove(connection)

    async def broadcast_to_delivery(self, message: dict):
        for connection in self.delivery_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                self.delivery_connections.remove(connection)

    async def broadcast_to_clients(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Define Models
class MenuItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str  # "pizzas", "burgers", "drinks", "sides"
    image_url: str
    available: bool = True
    preparation_time: int = 15  # minutes
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image_url: str
    available: bool = True
    preparation_time: int = 15

class CartItem(BaseModel):
    menu_item_id: str
    quantity: int
    special_instructions: Optional[str] = ""

class DeliveryInfo(BaseModel):
    customer_name: str
    customer_phone: str
    delivery_address: str
    delivery_zone: str  # "centro", "san_lorenzo", "lambare", etc.
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    items: List[CartItem]
    delivery_info: DeliveryInfo
    subtotal: float
    delivery_fee: float
    total: float
    status: str = "received"  # received, confirmed, preparing, ready, on_route, delivered, cancelled
    payment_method: str = "cash"  # cash, card, transfer
    estimated_delivery: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_delivery_person: Optional[str] = None
    delivery_notes: Optional[str] = ""

class OrderCreate(BaseModel):
    items: List[CartItem]
    delivery_info: DeliveryInfo
    payment_method: str = "cash"
    delivery_notes: Optional[str] = ""

class OrderStatusUpdate(BaseModel):
    status: str
    assigned_delivery_person: Optional[str] = None

class DeliveryPerson(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    phone: str
    is_available: bool = True
    current_orders: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DeliveryPersonCreate(BaseModel):
    name: str
    phone: str

# WebSocket endpoints
@app.websocket("/ws/admin")
async def websocket_admin_endpoint(websocket: WebSocket):
    await manager.connect(websocket, "admin")
    try:
        while True:
            data = await websocket.receive_text()
            # Handle admin messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket, "admin")

@app.websocket("/ws/delivery/{delivery_person_id}")
async def websocket_delivery_endpoint(websocket: WebSocket, delivery_person_id: str):
    await manager.connect(websocket, "delivery")
    try:
        while True:
            data = await websocket.receive_text()
            # Handle delivery person messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket, "delivery")

@app.websocket("/ws/client/{order_id}")
async def websocket_client_endpoint(websocket: WebSocket, order_id: str):
    await manager.connect(websocket, "client")
    try:
        while True:
            data = await websocket.receive_text()
            # Handle client messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket, "client")

# Menu Management
@api_router.post("/menu", response_model=MenuItem)
async def create_menu_item(item: MenuItemCreate):
    menu_item = MenuItem(**item.dict())
    await db.menu_items.insert_one(menu_item.dict())
    return menu_item

@api_router.get("/menu", response_model=List[MenuItem])
async def get_menu():
    menu_items = await db.menu_items.find({"available": True}).to_list(1000)
    return [MenuItem(**item) for item in menu_items]

@api_router.get("/menu/category/{category}", response_model=List[MenuItem])
async def get_menu_by_category(category: str):
    menu_items = await db.menu_items.find({"category": category, "available": True}).to_list(1000)
    return [MenuItem(**item) for item in menu_items]

@api_router.put("/menu/{item_id}", response_model=MenuItem)
async def update_menu_item(item_id: str, item: MenuItemCreate):
    updated_item = MenuItem(id=item_id, **item.dict())
    await db.menu_items.replace_one({"id": item_id}, updated_item.dict())
    return updated_item

@api_router.delete("/menu/{item_id}")
async def delete_menu_item(item_id: str):
    await db.menu_items.update_one({"id": item_id}, {"$set": {"available": False}})
    return {"message": "Menu item deleted successfully"}

# Order Management
@api_router.post("/orders", response_model=Order)
async def create_order(order_data: OrderCreate):
    # Calculate totals
    subtotal = 0
    for cart_item in order_data.items:
        menu_item = await db.menu_items.find_one({"id": cart_item.menu_item_id})
        if menu_item:
            subtotal += menu_item["price"] * cart_item.quantity
    
    # Calculate delivery fee based on zone
    delivery_fee = 15000 if order_data.delivery_info.delivery_zone == "centro" else 20000
    total = subtotal + delivery_fee
    
    # Calculate estimated delivery time (30-60 minutes)
    from datetime import timedelta
    estimated_delivery = datetime.utcnow().replace(microsecond=0) + timedelta(minutes=45)
    
    order = Order(
        items=order_data.items,
        delivery_info=order_data.delivery_info,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        total=total,
        payment_method=order_data.payment_method,
        estimated_delivery=estimated_delivery,
        delivery_notes=order_data.delivery_notes
    )
    
    await db.orders.insert_one(order.dict())
    
    # Broadcast new order to admins
    await manager.broadcast_to_admins({
        "type": "new_order",
        "order": order.dict()
    })
    
    return order

@api_router.get("/orders", response_model=List[Order])
async def get_orders():
    orders = await db.orders.find().sort("created_at", -1).to_list(1000)
    return [Order(**order) for order in orders]

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = await db.orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**order)

@api_router.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status_update: OrderStatusUpdate):
    order = await db.orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    update_data = {
        "status": status_update.status,
        "updated_at": datetime.utcnow()
    }
    
    if status_update.assigned_delivery_person:
        update_data["assigned_delivery_person"] = status_update.assigned_delivery_person
    
    await db.orders.update_one({"id": order_id}, {"$set": update_data})
    
    # Broadcast status update
    updated_order = await db.orders.find_one({"id": order_id})
    message = {
        "type": "order_status_update",
        "order_id": order_id,
        "status": status_update.status,
        "order": updated_order
    }
    
    await manager.broadcast_to_admins(message)
    await manager.broadcast_to_clients(message)
    if status_update.assigned_delivery_person:
        await manager.broadcast_to_delivery(message)
    
    return {"message": "Order status updated successfully"}

@api_router.get("/orders/status/{status}", response_model=List[Order])
async def get_orders_by_status(status: str):
    orders = await db.orders.find({"status": status}).sort("created_at", -1).to_list(1000)
    return [Order(**order) for order in orders]

# Delivery Person Management
@api_router.post("/delivery-persons", response_model=DeliveryPerson)
async def create_delivery_person(person_data: DeliveryPersonCreate):
    delivery_person = DeliveryPerson(**person_data.dict())
    await db.delivery_persons.insert_one(delivery_person.dict())
    return delivery_person

@api_router.get("/delivery-persons", response_model=List[DeliveryPerson])
async def get_delivery_persons():
    persons = await db.delivery_persons.find().to_list(1000)
    return [DeliveryPerson(**person) for person in persons]

@api_router.get("/delivery-persons/available", response_model=List[DeliveryPerson])
async def get_available_delivery_persons():
    persons = await db.delivery_persons.find({"is_available": True}).to_list(1000)
    return [DeliveryPerson(**person) for person in persons]

# Analytics endpoints
@api_router.get("/analytics/today")
async def get_today_analytics():
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Total orders today
    total_orders = await db.orders.count_documents({
        "created_at": {"$gte": today}
    })
    
    # Total revenue today
    revenue_pipeline = [
        {"$match": {"created_at": {"$gte": today}, "status": {"$ne": "cancelled"}}},
        {"$group": {"_id": None, "total_revenue": {"$sum": "$total"}}}
    ]
    revenue_result = await db.orders.aggregate(revenue_pipeline).to_list(1)
    total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
    
    # Orders by status
    status_pipeline = [
        {"$match": {"created_at": {"$gte": today}}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    status_results = await db.orders.aggregate(status_pipeline).to_list(10)
    orders_by_status = {result["_id"]: result["count"] for result in status_results}
    
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "orders_by_status": orders_by_status,
        "date": today.isoformat()
    }

# Initialize sample menu data
@api_router.post("/initialize-menu")
async def initialize_sample_menu():
    sample_menu = [
        {
            "name": "Pizza Margherita",
            "description": "Clásica pizza con tomate, mozzarella y albahaca fresca",
            "price": 75000,
            "category": "pizzas",
            "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwyfHxwaXp6YXxlbnwwfHx8fDE3NTQzOTkxNjl8MA&ixlib=rb-4.1.0&q=85",
            "preparation_time": 15
        },
        {
            "name": "Pizza Pepperoni",
            "description": "Pizza con pepperoni, mozzarella y salsa de tomate",
            "price": 85000,
            "category": "pizzas", 
            "image_url": "https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw0fHxwaXp6YXxlbnwwfHx8fDE3NTQzOTkxNjl8MA&ixlib=rb-4.1.0&q=85",
            "preparation_time": 15
        },
        {
            "name": "Pizza Hawaiana",
            "description": "Pizza con jamón, piña, mozzarella y salsa de tomate",
            "price": 80000,
            "category": "pizzas",
            "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwyfHxwaXp6YXxlbnwwfHx8fDE3NTQzOTkxNjl8MA&ixlib=rb-4.1.0&q=85",
            "preparation_time": 15
        },
        {
            "name": "Hamburguesa Clásica",
            "description": "Carne de res, lechuga, tomate, cebolla y salsa especial",
            "price": 45000,
            "category": "hamburguesas",
            "image_url": "https://images.pexels.com/photos/3023476/pexels-photo-3023476.jpeg",
            "preparation_time": 12
        },
        {
            "name": "Coca Cola 500ml",
            "description": "Bebida gaseosa Coca Cola",
            "price": 8000,
            "category": "bebidas",
            "image_url": "https://images.pexels.com/photos/3023476/pexels-photo-3023476.jpeg",
            "preparation_time": 1
        },
        {
            "name": "Papas Fritas",
            "description": "Papas fritas crujientes con sal",
            "price": 15000,
            "category": "acompañamientos",
            "image_url": "https://images.pexels.com/photos/3023476/pexels-photo-3023476.jpeg",
            "preparation_time": 8
        }
    ]
    
    # Clear existing menu and add sample items
    await db.menu_items.delete_many({})
    for item_data in sample_menu:
        menu_item = MenuItem(**item_data)
        await db.menu_items.insert_one(menu_item.dict())
    
    return {"message": "Sample menu initialized successfully"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()