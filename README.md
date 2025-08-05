# PizzApp - Sistema de Gestión de Pizzería

![PizzApp Logo](https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwyfHxwaXp6YXxlbnwwfHx8fDE3NTQzOTkxNjl8MA&ixlib=rb-4.1.0&q=85&w=400)

PizzApp es una aplicación web completa para la gestión de pizzerías y restaurantes de comida rápida. Diseñada específicamente para el mercado paraguayo, incluye gestión de pedidos en tiempo real, autenticación basada en roles, y dashboards especializados para diferentes tipos de usuarios.

## 📋 Descripción del Proyecto

PizzApp digitaliza y optimiza todo el proceso operativo de una pizzería, desde la gestión del menú hasta la entrega final. Incluye:

- **Sistema de pedidos online** con carrito de compras
- **Gestión de roles** (Admin, Manager, Kitchen, Delivery)
- **Dashboards especializados** para cada tipo de usuario
- **Seguimiento en tiempo real** de pedidos
- **Analytics y reportes** de ventas
- **Gestión de zonas de entrega** para Paraguay
- **Interfaz moderna y responsive**

## 🏗️ Estructura de Archivos

```
PizzApp/
├── backend/                    # API FastAPI
│   ├── server.py              # Aplicación principal y endpoints
│   ├── requirements.txt       # Dependencias Python
│   └── .env                   # Variables de entorno (backend)
├── frontend/                  # Aplicación React
│   ├── src/
│   │   ├── App.js            # Componente principal y rutas
│   │   ├── App.css           # Estilos globales
│   │   ├── index.js          # Punto de entrada React
│   │   ├── index.css         # Estilos base y Tailwind
│   │   └── components/ui/    # Componentes UI (Shadcn)
│   ├── public/               # Archivos estáticos
│   ├── package.json          # Dependencias Node.js
│   ├── tailwind.config.js    # Configuración Tailwind CSS
│   └── .env                  # Variables de entorno (frontend)
├── tests/                    # Archivos de pruebas
├── docs/                     # Documentación adicional
└── README.md                 # Este archivo
```

## 🔧 Prerrequisitos

### Software Requerido
- **Python 3.11+** - Para el backend FastAPI
- **Node.js 18+** - Para el frontend React
- **MongoDB 5.0+** - Base de datos principal
- **Yarn 1.22+** - Gestor de paquetes (requerido)

### Servicios Externos
- **Base de datos MongoDB** (local o MongoDB Atlas)
- **Servidor web** para deployment (opcional)

## 🚀 Instalación

### 1. Clonar el Repositorio
```bash
git clone <tu-repositorio>
cd pizzapp
```

### 2. Configurar Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Frontend
```bash
cd frontend

# Instalar dependencias (USAR YARN, NO NPM)
yarn install
```

## ⚙️ Configuración

### Variables de Entorno Backend (`backend/.env`)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=pizzapp_db
SECRET_KEY=your-super-secret-jwt-key-change-in-production
```

### Variables de Entorno Frontend (`frontend/.env`)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### Configuración de MongoDB
1. **Instalar MongoDB** localmente o usar MongoDB Atlas
2. **Crear base de datos** llamada `pizzapp_db`
3. **No requiere configuración adicional** - las colecciones se crean automáticamente

## 🏃‍♂️ Ejecución

### Desarrollo Local

#### 1. Iniciar Backend
```bash
cd backend
source venv/bin/activate  # Activar entorno virtual
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```
El backend estará disponible en: `http://localhost:8001`

#### 2. Iniciar Frontend
```bash
cd frontend
yarn start
```
El frontend estará disponible en: `http://localhost:3000`

### Producción
```bash
# Backend
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001

# Frontend
cd frontend
yarn build
# Servir archivos de build/ con tu servidor web preferido
```

## 👥 Usuarios por Defecto

El sistema incluye usuarios predefinidos para testing:

| Usuario | Contraseña | Rol | Acceso |
|---------|------------|-----|--------|
| `admin` | `admin123` | Admin | Acceso completo al sistema |
| `manager` | `manager123` | Manager | Gestión operativa |
| `kitchen` | `kitchen123` | Kitchen | Solo gestión de cocina |
| `delivery` | `delivery123` | Delivery | Solo gestión de entregas |

**Para crear usuarios por defecto:**
1. Ir a `/login`
2. Hacer clic en "Crear Usuarios por Defecto"

## 🔗 API Reference

### Autenticación

#### POST `/api/auth/login`
Iniciar sesión de usuario
```bash
curl -X POST "http://localhost:8001/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```

#### GET `/api/auth/me`
Obtener información del usuario actual
```bash
curl -X GET "http://localhost:8001/api/auth/me" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Menú

#### GET `/api/menu`
Obtener todos los productos del menú
```bash
curl -X GET "http://localhost:8001/api/menu"
```

#### POST `/api/menu`
Crear nuevo producto (requiere rol Admin/Manager)
```bash
curl -X POST "http://localhost:8001/api/menu" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "name": "Pizza Margherita",
       "description": "Pizza clásica con tomate y mozzarella",
       "price": 75000,
       "category": "pizzas",
       "image_url": "https://example.com/pizza.jpg",
       "preparation_time": 15
     }'
```

### Pedidos

#### POST `/api/orders`
Crear nuevo pedido (público)
```bash
curl -X POST "http://localhost:8001/api/orders" \
     -H "Content-Type: application/json" \
     -d '{
       "items": [
         {
           "menu_item_id": "item-uuid",
           "quantity": 2,
           "special_instructions": "Extra cheese"
         }
       ],
       "delivery_info": {
         "customer_name": "Juan Pérez",
         "customer_phone": "0981123456",
         "delivery_address": "Av. España 123, Asunción",
         "delivery_zone": "centro"
       },
       "payment_method": "cash",
       "delivery_notes": "Tocar timbre"
     }'
```

#### GET `/api/orders`
Obtener pedidos (filtrado por rol)
```bash
curl -X GET "http://localhost:8001/api/orders" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### PUT `/api/orders/{order_id}/status`
Actualizar estado del pedido
```bash
curl -X PUT "http://localhost:8001/api/orders/ORDER_ID/status" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"status": "confirmed"}'
```

### Analytics

#### GET `/api/analytics/today`
Obtener estadísticas del día (Admin/Manager)
```bash
curl -X GET "http://localhost:8001/api/analytics/today" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🎭 Sistema de Roles

### 👑 Admin
- **Acceso completo** al sistema
- **Gestión de usuarios** y roles
- **Analytics completos**
- **Configuración** del sistema

### 👔 Manager
- **Gestión operativa** completa
- **Analytics y reportes**
- **Control de pedidos** y menú
- **Sin gestión de usuarios**

### 👨‍🍳 Kitchen (Cocina)
- **Solo pedidos de preparación**
- **Estados**: received → confirmed → preparing → ready
- **Sin acceso** a entregas o analytics

### 🚚 Delivery
- **Solo pedidos de entrega**
- **Estados**: ready → on_route → delivered
- **Información de cliente** y direcciones

## 🌍 Configuración Paraguay

### Zonas de Entrega
- **Centro**: 15.000 ₲
- **San Lorenzo**: 20.000 ₲
- **Lambaré**: 20.000 ₲
- **Fernando de la Mora**: 20.000 ₲

### Moneda
- Precios en **Guaraníes (PYG)**
- Formato: `Gs. 75.000`

### Horarios
- **Atención**: 18:00 - 23:30
- **Delivery**: Hasta medianoche

## 🧪 Testing

### Ejecutar Tests Backend
```bash
cd backend
python -m pytest tests/ -v
```

### Ejecutar Tests Frontend
```bash
cd frontend
yarn test
```

### Tests Manuales
1. **Crear pedido** desde la interfaz web
2. **Probar roles** con diferentes usuarios
3. **Verificar dashboard** en tiempo real
4. **Comprobar estados** de pedidos

## 🚀 Deployment

### Requisitos de Producción
- **MongoDB** configurado y accesible
- **Variables de entorno** configuradas
- **SECRET_KEY** único y seguro
- **CORS** configurado para tu dominio

### Variables de Entorno Producción
```env
# Backend
MONGO_URL=mongodb://tu-servidor-mongo:27017
DB_NAME=pizzapp_production
SECRET_KEY=tu-secret-key-super-seguro-y-largo

# Frontend
REACT_APP_BACKEND_URL=https://tu-dominio.com
```

## 🔒 Seguridad

- **JWT Authentication** con tokens de 30 minutos
- **Hashing bcrypt** para contraseñas
- **Validación de roles** en cada endpoint
- **CORS configurado** para origen específico
- **Validación Pydantic** en todos los inputs

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno
- **MongoDB** - Base de datos NoSQL
- **Motor** - Driver MongoDB asíncrono
- **JWT** - Autenticación de tokens
- **Bcrypt** - Hashing de contraseñas
- **Pydantic** - Validación de datos

### Frontend
- **React 19** - Biblioteca de UI
- **React Router** - Navegación
- **Axios** - Cliente HTTP
- **Tailwind CSS** - Framework CSS
- **Shadcn/ui** - Componentes UI
- **Lucide React** - Iconos

## 📈 Roadmap Futuro

### Versión 2.0
- [ ] **Notificaciones WhatsApp** (Twilio)
- [ ] **Pagos en línea** (Stripe/MercadoPago)
- [ ] **Múltiples sucursales**
- [ ] **App móvil** (React Native)

### Versión 2.1
- [ ] **Programa de fidelización**
- [ ] **Pedidos programados**
- [ ] **Integración contable**
- [ ] **Reportes avanzados**

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Crear rama** para feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abrir Pull Request**

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

¿Necesitas ayuda? Contacta con:
- **Email**: support@pizzapp.com
- **GitHub Issues**: [Crear issue](../../issues)
- **Documentación**: [Wiki del proyecto](../../wiki)

---

**Desarrollado con ❤️ para pizzerías paraguayas**