# Guía para Desarrolladores - PizzApp

## 🚀 Configuración del Entorno de Desarrollo

### Paso a Paso para Nuevos Desarrolladores

#### 1. Requisitos del Sistema
```bash
# Verificar versiones instaladas
python --version  # Debe ser >= 3.11
node --version    # Debe ser >= 18.0
npm --version     # Para verificar Node.js
yarn --version    # Debe estar instalado (npm install -g yarn)
mongo --version   # MongoDB >= 5.0
```

#### 2. Configuración Inicial
```bash
# Clonar repositorio
git clone <repository-url>
cd pizzapp

# Configurar backend
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configurar frontend
cd ../frontend
yarn install
```

#### 3. Variables de Entorno
```bash
# Copiar archivos de ejemplo
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Editar con valores reales
nano backend/.env
nano frontend/.env
```

## 🏗️ Arquitectura del Código

### Backend (FastAPI)

#### Estructura de Archivos
```
backend/
├── server.py          # Aplicación principal
├── requirements.txt   # Dependencias Python
├── .env              # Variables de entorno
└── .env.example      # Plantilla de variables
```

#### Patrones de Código Backend

**1. Definición de Endpoints**
```python
@api_router.get("/endpoint", response_model=ResponseModel)
async def endpoint_function(param: ParamType = Depends(dependency)):
    """
    Descripción del endpoint en español.
    
    Args:
        param (ParamType): Descripción del parámetro
        
    Returns:
        ResponseModel: Descripción de la respuesta
        
    Raises:
        HTTPException: Condiciones de error
    """
    # Lógica del endpoint
    return response
```

**2. Modelos Pydantic**
```python
class ModelName(BaseModel):
    """
    Descripción del modelo.
    
    Attributes:
        field_name (type): Descripción del campo
    """
    field_name: type = Field(description="Descripción")
```

**3. Autenticación y Roles**
```python
# Para endpoints que requieren autenticación
@api_router.post("/protected-endpoint")
async def protected_endpoint(
    current_user: AdminUser = Depends(require_role(["admin", "manager"]))
):
    # Solo admins y managers pueden acceder
    pass
```

### Frontend (React)

#### Estructura de Componentes
```
frontend/src/
├── App.js              # Componente principal y rutas
├── App.css             # Estilos globales
├── index.js            # Punto de entrada
├── index.css           # Estilos base
└── components/ui/      # Componentes UI (Shadcn)
```

#### Patrones de Código Frontend

**1. Componentes Funcionales**
```javascript
/**
 * Componente para [descripción]
 * 
 * @param {Object} props - Propiedades del componente
 * @param {string} props.propName - Descripción de la prop
 * @returns {React.Component} Componente renderizado
 */
const ComponentName = ({ propName }) => {
  // Lógica del componente
  return <div>{propName}</div>;
};
```

**2. Hooks Personalizados**
```javascript
/**
 * Hook personalizado para [funcionalidad]
 * 
 * @returns {Object} Estado y funciones del hook
 */
const useCustomHook = () => {
  const [state, setState] = useState(null);
  
  // Lógica del hook
  
  return { state, setState };
};
```

## 🔧 APIs y Endpoints

### Autenticación
```bash
# Login
POST /api/auth/login
Body: {"username": "admin", "password": "admin123"}

# Obtener info del usuario
GET /api/auth/me
Headers: Authorization: Bearer <token>

# Crear usuarios por defecto
POST /api/auth/init-admin
```

### Menú
```bash
# Obtener menú completo
GET /api/menu

# Crear producto (Admin/Manager)
POST /api/menu
Headers: Authorization: Bearer <token>
Body: {
  "name": "Pizza Margherita",
  "description": "Pizza clásica",
  "price": 75000,
  "category": "pizzas",
  "image_url": "https://...",
  "preparation_time": 15
}
```

### Pedidos
```bash
# Crear pedido (público)
POST /api/orders
Body: {
  "items": [{"menu_item_id": "uuid", "quantity": 2}],
  "delivery_info": {
    "customer_name": "Juan Pérez",
    "customer_phone": "0981123456",
    "delivery_address": "Av. España 123",
    "delivery_zone": "centro"
  }
}

# Obtener pedidos (filtrado por rol)
GET /api/orders
Headers: Authorization: Bearer <token>

# Actualizar estado
PUT /api/orders/{order_id}/status
Headers: Authorization: Bearer <token>
Body: {"status": "confirmed"}
```

## 🎨 Estilos y UI

### Tailwind CSS
```javascript
// Clases comunes utilizadas
const commonClasses = {
  button: "bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white py-3 px-6 rounded-xl font-semibold transition-all duration-300",
  card: "bg-white rounded-2xl shadow-lg p-6",
  input: "w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent"
};
```

### Componentes Shadcn/ui
```javascript
// Componentes disponibles en /components/ui/
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Card } from './components/ui/card';
```

## 🧪 Testing y Debugging

### Backend Testing
```bash
# Ejecutar tests
cd backend
python -m pytest tests/ -v

# Test específico
python -m pytest tests/test_auth.py -v

# Con coverage
python -m pytest tests/ --cov=server
```

### Frontend Testing
```bash
# Ejecutar tests
cd frontend
yarn test

# Tests en modo watch
yarn test --watch

# Coverage
yarn test --coverage
```

### Debugging

**Backend (FastAPI)**
```python
# Logging
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")

# Debugging con pdb
import pdb; pdb.set_trace()
```

**Frontend (React)**
```javascript
// Console logging
console.log("Debug:", variable);
console.table(arrayData);

// React Developer Tools
// Instalar extensión del navegador
```

## 🔍 Solución de Problemas Comunes

### Error: "ModuleNotFoundError" (Backend)
```bash
# Verificar que el entorno virtual está activado
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Module parse failed" (Frontend)
```bash
# Limpiar cache
yarn cache clean

# Reinstalar node_modules
rm -rf node_modules yarn.lock
yarn install
```

### Error: "MongoDB connection failed"
```bash
# Verificar que MongoDB está corriendo
sudo systemctl status mongod

# Iniciar MongoDB
sudo systemctl start mongod

# Verificar conexión
mongo --eval "db.stats()"
```

### Error: "JWT token invalid"
```bash
# El token puede haber expirado (30 minutos)
# Hacer login nuevamente
curl -X POST "http://localhost:8001/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```

## 📊 Base de Datos

### Colecciones MongoDB

#### admin_users
```javascript
{
  "_id": ObjectId,
  "id": "uuid-string",
  "username": "admin",
  "email": "admin@pizzapp.com",
  "hashed_password": "bcrypt-hash",
  "role": "admin",
  "is_active": true,
  "created_at": ISODate
}
```

#### menu_items
```javascript
{
  "_id": ObjectId,
  "id": "uuid-string",
  "name": "Pizza Margherita",
  "description": "Pizza clásica",
  "price": 75000,
  "category": "pizzas",
  "image_url": "https://...",
  "available": true,
  "preparation_time": 15,
  "created_at": ISODate
}
```

#### orders
```javascript
{
  "_id": ObjectId,
  "id": "uuid-string",
  "items": [
    {
      "menu_item_id": "uuid",
      "quantity": 2,
      "special_instructions": ""
    }
  ],
  "delivery_info": {
    "customer_name": "Juan Pérez",
    "customer_phone": "0981123456",
    "delivery_address": "Av. España 123",
    "delivery_zone": "centro"
  },
  "subtotal": 150000,
  "delivery_fee": 15000,
  "total": 165000,
  "status": "received",
  "payment_method": "cash",
  "estimated_delivery": ISODate,
  "created_at": ISODate,
  "updated_at": ISODate
}
```

## 📈 Performance y Optimización

### Backend Optimizations
```python
# Usar índices en MongoDB
await db.orders.create_index("created_at")
await db.orders.create_index("status")
await db.admin_users.create_index("username", unique=True)

# Limitar resultados de consultas
orders = await db.orders.find().limit(100).to_list(100)
```

### Frontend Optimizations
```javascript
// Lazy loading de componentes
const AdminDashboard = React.lazy(() => import('./AdminDashboard'));

// Memoización de componentes costosos
const ExpensiveComponent = React.memo(({ data }) => {
  // Componente costoso
});

// useCallback para funciones
const handleClick = useCallback(() => {
  // Handle click
}, [dependency]);
```

## 🚀 Deployment

### Desarrollo Local
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Terminal 2: Frontend
cd frontend
yarn start
```

### Build de Producción
```bash
# Backend
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001

# Frontend
cd frontend
yarn build
# Servir archivos de build/ con servidor web
```

## 📝 Convenciones de Código

### Python (Backend)
- **PEP 8** para estilo de código
- **Type hints** obligatorios en funciones nuevas
- **Docstrings** en español para todas las funciones públicas
- **Nombres descriptivos** en español/inglés según contexto

### JavaScript (Frontend)
- **ES6+** sintaxis moderna
- **JSDoc** para documentación de funciones
- **Componentes funcionales** con hooks
- **Nombres en camelCase** para variables y funciones

### Git
```bash
# Formato de commits
feat: agregar autenticación JWT
fix: corregir cálculo de precios
docs: actualizar README
style: formatear código con prettier
```

## 🔗 Recursos Útiles

### Documentación
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [MongoDB Docs](https://docs.mongodb.com/)

### Herramientas
- **MongoDB Compass**: GUI para MongoDB
- **Postman**: Testing de APIs
- **React DevTools**: Debugging React
- **VS Code**: Editor recomendado

### Extensions VS Code Recomendadas
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.pylint",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-thunder-client"
  ]
}
```

---

**¿Preguntas?** Consulta la documentación principal en [README.md](README.md) o crea un issue en el repositorio.