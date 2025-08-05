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

# Security configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

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

# Authentication Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_admin_user(username: str):
    admin = await db.admin_users.find_one({"username": username})
    if admin:
        return AdminUser(**admin)
    return None

async def authenticate_admin(username: str, password: str):
    admin = await get_admin_user(username)
    if not admin:
        return False
    if not verify_password(password, admin.hashed_password):
        return False
    return admin

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    admin = await get_admin_user(username=token_data.username)
    if admin is None:
        raise credentials_exception
    return admin

# Role-based access control functions
def require_role(allowed_roles: List[str]):
    def role_checker(current_admin: AdminUser = Depends(get_current_admin)):
        if current_admin.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        return current_admin
    return role_checker

# Role dependencies
AdminOnly = Depends(require_role(["admin"]))
AdminOrManager = Depends(require_role(["admin", "manager"]))
KitchenStaff = Depends(require_role(["admin", "manager", "kitchen"]))
DeliveryStaff = Depends(require_role(["admin", "manager", "delivery"]))
AllRoles = Depends(require_role(["admin", "manager", "kitchen", "delivery"]))

# Define Models

# Authentication Models
class AdminUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    hashed_password: str
    role: str = "admin"  # admin, manager, kitchen, delivery
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "admin"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

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

# Authentication endpoints
@api_router.post("/auth/login", response_model=Token)
async def login_admin(login_data: LoginRequest):
    admin = await authenticate_admin(login_data.username, login_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.post("/auth/create-admin", response_model=dict)
async def create_admin_user(admin_data: AdminUserCreate):
    # Check if admin already exists
    existing_admin = await get_admin_user(admin_data.username)
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin user already exists")
    
    # Create admin user
    hashed_password = get_password_hash(admin_data.password)
    admin_user = AdminUser(
        username=admin_data.username,
        email=admin_data.email,
        hashed_password=hashed_password
    )
    
    await db.admin_users.insert_one(admin_user.dict())
    return {"message": "Admin user created successfully"}

@api_router.get("/auth/me", response_model=dict)
async def read_admin_me(current_admin: AdminUser = Depends(get_current_admin)):
    return {
        "username": current_admin.username,
        "email": current_admin.email,
        "role": current_admin.role,
        "is_active": current_admin.is_active
    }

@api_router.post("/auth/init-admin")
async def initialize_default_admin():
    """Initialize default admin user for testing"""
    default_users = [
        {"username": "admin", "password": "admin123", "role": "admin", "email": "admin@pizzapp.com"},
        {"username": "manager", "password": "manager123", "role": "manager", "email": "manager@pizzapp.com"},
        {"username": "kitchen", "password": "kitchen123", "role": "kitchen", "email": "kitchen@pizzapp.com"},
        {"username": "delivery", "password": "delivery123", "role": "delivery", "email": "delivery@pizzapp.com"}
    ]
    
    created_users = []
    existing_users = []
    
    for user_data in default_users:
        existing_user = await get_admin_user(user_data["username"])
        if existing_user:
            existing_users.append(user_data["username"])
            continue
        
        # Create user
        hashed_password = get_password_hash(user_data["password"])
        admin_user = AdminUser(
            username=user_data["username"],
            email=user_data["email"],
            role=user_data["role"],
            hashed_password=hashed_password
        )
        
        await db.admin_users.insert_one(admin_user.dict())
        created_users.append({
            "username": user_data["username"],
            "password": user_data["password"],
            "role": user_data["role"]
        })
    
    return {
        "message": "Default users initialization completed",
        "created_users": created_users,
        "existing_users": existing_users
    }

# Menu Management (Admin/Manager only)
@api_router.post("/menu", response_model=MenuItem)
async def create_menu_item(item: MenuItemCreate, current_admin: AdminUser = Depends(require_role(["admin", "manager"]))):
    menu_item = MenuItem(**item.dict())
    await db.menu_items.insert_one(menu_item.dict())
    return menu_item

@api_router.get("/menu", response_model=List[MenuItem])
async def get_menu():
    # Public endpoint - no auth required
    menu_items = await db.menu_items.find({"available": True}).to_list(1000)
    return [MenuItem(**item) for item in menu_items]

@api_router.get("/menu/category/{category}", response_model=List[MenuItem])
async def get_menu_by_category(category: str):
    # Public endpoint - no auth required
    menu_items = await db.menu_items.find({"category": category, "available": True}).to_list(1000)
    return [MenuItem(**item) for item in menu_items]

@api_router.put("/menu/{item_id}", response_model=MenuItem)
async def update_menu_item(item_id: str, item: MenuItemCreate, current_admin: AdminUser = Depends(require_role(["admin", "manager"]))):
    updated_item = MenuItem(id=item_id, **item.dict())
    await db.menu_items.replace_one({"id": item_id}, updated_item.dict())
    return updated_item

@api_router.delete("/menu/{item_id}")
async def delete_menu_item(item_id: str, current_admin: AdminUser = Depends(require_role(["admin", "manager"]))):
    await db.menu_items.update_one({"id": item_id}, {"$set": {"available": False}})
    return {"message": "Menu item deleted successfully"}

# Order Management with role-based access
@api_router.post("/orders", response_model=Order)
async def create_order(order_data: OrderCreate):
    # Public endpoint - customers can create orders
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
async def get_orders(current_admin: AdminUser = Depends(require_role(["admin", "manager", "kitchen", "delivery"]))):
    # Role-based filtering
    if current_admin.role == "kitchen":
        # Kitchen only sees orders that need preparation
        orders = await db.orders.find({
            "status": {"$in": ["received", "confirmed", "preparing", "ready"]}
        }).sort("created_at", -1).to_list(1000)
    elif current_admin.role == "delivery":
        # Delivery only sees orders ready for delivery
        orders = await db.orders.find({
            "status": {"$in": ["ready", "on_route", "delivered"]}
        }).sort("created_at", -1).to_list(1000)
    else:
        # Admin and Manager see all orders
        orders = await db.orders.find().sort("created_at", -1).to_list(1000)
    
    return [Order(**order) for order in orders]

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    # Public endpoint for order tracking
    order = await db.orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**order)

@api_router.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status_update: OrderStatusUpdate, current_admin: AdminUser = Depends(require_role(["admin", "manager", "kitchen", "delivery"]))):
    order = await db.orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Role-based status update restrictions
    current_status = order["status"]
    new_status = status_update.status
    
    # Kitchen staff can only update certain statuses
    if current_admin.role == "kitchen":
        allowed_transitions = {
            "received": ["confirmed", "cancelled"],
            "confirmed": ["preparing", "cancelled"],
            "preparing": ["ready", "cancelled"]
        }
        if current_status not in allowed_transitions or new_status not in allowed_transitions[current_status]:
            raise HTTPException(
                status_code=403, 
                detail=f"Kitchen staff cannot change status from {current_status} to {new_status}"
            )
    
    # Delivery staff can only update delivery-related statuses
    elif current_admin.role == "delivery":
        allowed_transitions = {
            "ready": ["on_route"],
            "on_route": ["delivered"]
        }
        if current_status not in allowed_transitions or new_status not in allowed_transitions[current_status]:
            raise HTTPException(
                status_code=403, 
                detail=f"Delivery staff cannot change status from {current_status} to {new_status}"
            )
    
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
async def get_orders_by_status(status: str, current_admin: AdminUser = Depends(require_role(["admin", "manager", "kitchen", "delivery"]))):
    # Role-based filtering combined with status filter
    query = {"status": status}
    
    if current_admin.role == "kitchen":
        # Kitchen only sees preparation-related statuses
        if status not in ["received", "confirmed", "preparing", "ready"]:
            return []
        orders = await db.orders.find(query).sort("created_at", -1).to_list(1000)
    elif current_admin.role == "delivery":
        # Delivery only sees delivery-related statuses
        if status not in ["ready", "on_route", "delivered"]:
            return []
        orders = await db.orders.find(query).sort("created_at", -1).to_list(1000)
    else:
        # Admin and Manager see all
        orders = await db.orders.find(query).sort("created_at", -1).to_list(1000)
    
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

# Analytics endpoints (Admin and Manager only)
@api_router.get("/analytics/today")
async def get_today_analytics(current_admin: AdminUser = Depends(require_role(["admin", "manager"]))):
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

# User Management (Admin only)
@api_router.get("/users", response_model=List[dict])
async def get_all_users(current_admin: AdminUser = Depends(require_role(["admin"]))):
    users = await db.admin_users.find().to_list(1000)
    return [{
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "is_active": user["is_active"],
        "created_at": user["created_at"]
    } for user in users]

@api_router.post("/users", response_model=dict)
async def create_user(user_data: AdminUserCreate, current_admin: AdminUser = AdminOnly):
    # Check if user already exists
    existing_user = await get_admin_user(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    new_user = AdminUser(
        username=user_data.username,
        email=user_data.email,
        role=user_data.role,
        hashed_password=hashed_password
    )
    
    await db.admin_users.insert_one(new_user.dict())
    return {"message": "User created successfully"}

@api_router.put("/users/{user_id}/role")
async def update_user_role(user_id: str, new_role: str, current_admin: AdminUser = AdminOnly):
    valid_roles = ["admin", "manager", "kitchen", "delivery"]
    if new_role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {valid_roles}")
    
    result = await db.admin_users.update_one(
        {"id": user_id},
        {"$set": {"role": new_role}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User role updated successfully"}

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