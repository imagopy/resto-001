# Documentación de Dependencias - PizzApp

## 📋 Resumen de Tecnologías

### Stack Principal
- **Backend**: FastAPI + MongoDB + JWT Auth
- **Frontend**: React 19 + Tailwind CSS + Shadcn/ui
- **Base de Datos**: MongoDB 5.0+
- **Autenticación**: JWT con bcrypt
- **Comunicación**: REST API + WebSockets

---

## 🐍 Dependencias Backend (Python)

### Core Framework
```txt
fastapi==0.110.1              # Framework web asíncrono moderno
uvicorn==0.25.0               # Servidor ASGI para FastAPI
pydantic>=2.6.4               # Validación de datos y serialización
```

### Base de Datos
```txt
pymongo==4.5.0                # Driver oficial de MongoDB
motor==3.3.1                  # Driver asíncrono de MongoDB
```

### Autenticación y Seguridad
```txt
python-jose[cryptography]>=3.3.0  # Manejo de tokens JWT
pyjwt>=2.10.1                     # Biblioteca JWT alternativa
passlib[bcrypt]>=1.7.4             # Hashing de contraseñas
bcrypt>=4.0.0                      # Algoritmo de hashing seguro
cryptography>=42.0.8              # Criptografía de bajo nivel
```

### Configuración y Entorno
```txt
python-dotenv>=1.0.1          # Carga de variables de entorno
tzdata>=2024.2                # Datos de zona horaria
```

### Validación y Parseo
```txt
email-validator>=2.2.0        # Validación de emails
python-multipart>=0.0.9       # Soporte para form-data
```

### HTTP y Requests
```txt
requests>=2.31.0              # Cliente HTTP
requests-oauthlib>=2.0.0      # OAuth para requests
```

### Desarrollo y Testing
```txt
pytest>=8.0.0                 # Framework de testing
black>=24.1.1                 # Formateador de código
isort>=5.13.2                 # Ordenador de imports
flake8>=7.0.0                 # Linter de código
mypy>=1.8.0                   # Verificador de tipos estático
```

### Análisis de Datos (Para Analytics)
```txt
pandas>=2.2.0                 # Manipulación de datos
numpy>=1.26.0                 # Computación numérica
```

### Utilidades
```txt
boto3>=1.34.129               # AWS SDK (futuro uso)
jq>=1.6.0                     # Procesador JSON
typer>=0.9.0                  # CLI framework
```

---

## ⚛️ Dependencias Frontend (Node.js)

### Core Framework
```json
{
  "react": "^19.0.0",                    // Biblioteca principal de UI
  "react-dom": "^19.0.0",               // DOM renderer para React
  "react-scripts": "5.0.1",             // Scripts de Create React App
  "react-router-dom": "^7.5.1"          // Routing para SPA
}
```

### HTTP Client
```json
{
  "axios": "^1.8.4"                     // Cliente HTTP para API calls
}
```

### UI Components (Shadcn/ui)
```json
{
  "@radix-ui/react-accordion": "^1.2.8",
  "@radix-ui/react-alert-dialog": "^1.1.11",
  "@radix-ui/react-aspect-ratio": "^1.1.4",
  "@radix-ui/react-avatar": "^1.1.7",
  "@radix-ui/react-checkbox": "^1.2.3",
  "@radix-ui/react-collapsible": "^1.1.8",
  "@radix-ui/react-context-menu": "^2.2.12",
  "@radix-ui/react-dialog": "^1.1.11",
  "@radix-ui/react-dropdown-menu": "^2.1.12",
  "@radix-ui/react-hover-card": "^1.1.11",
  "@radix-ui/react-label": "^2.1.4",
  "@radix-ui/react-menubar": "^1.1.12",
  "@radix-ui/react-navigation-menu": "^1.2.10",
  "@radix-ui/react-popover": "^1.1.11",
  "@radix-ui/react-progress": "^1.1.4",
  "@radix-ui/react-radio-group": "^1.3.4",
  "@radix-ui/react-scroll-area": "^1.2.6",
  "@radix-ui/react-select": "^2.2.2",
  "@radix-ui/react-separator": "^1.1.4",
  "@radix-ui/react-slider": "^1.3.2",
  "@radix-ui/react-slot": "^1.2.0",
  "@radix-ui/react-switch": "^1.2.2",
  "@radix-ui/react-tabs": "^1.1.9",
  "@radix-ui/react-toast": "^1.2.11",
  "@radix-ui/react-toggle": "^1.1.6",
  "@radix-ui/react-toggle-group": "^1.1.7",
  "@radix-ui/react-tooltip": "^1.2.4"
}
```

### Estilos y CSS
```json
{
  "tailwindcss": "^3.4.0",              // Framework CSS utility-first
  "autoprefixer": "^10.4.0",           // PostCSS plugin para prefijos
  "postcss": "^8.4.0",                 // Procesador CSS
  "class-variance-authority": "^0.7.1", // Utilidad para clases dinámicas
  "clsx": "^2.1.1"                     // Utilidad para clases condicionales
}
```

### Forms y Validación
```json
{
  "react-hook-form": "^7.56.2",        // Manejo de formularios
  "@hookform/resolvers": "^5.0.1"      // Resolvers para validación
}
```

### Iconos
```json
{
  "lucide-react": "^0.507.0"           // Iconos SVG modernos
}
```

### Utilidades UI
```json
{
  "date-fns": "^4.1.0",                // Manipulación de fechas
  "react-day-picker": "8.10.1",        // Selector de fechas
  "cmdk": "^1.1.1",                    // Command palette component
  "input-otp": "^1.4.2",               // Input para códigos OTP
  "embla-carousel-react": "^8.6.0",    // Carrusel de imágenes
  "react-resizable-panels": "^3.0.1",  // Paneles redimensionables
  "next-themes": "^0.4.6"              // Manejo de temas (dark/light)
}
```

### Development Tools
```json
{
  "@types/node": "^16.18.0",           // Tipos TypeScript para Node.js
  "sonner": "^1.7.1",                 // Notificaciones toast
  "vaul": "^1.1.1"                    // Drawer component
}
```

---

## 🔧 Scripts y Comandos

### Backend Scripts
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Ejecutar tests
python -m pytest tests/ -v

# Formatear código
black server.py
isort server.py

# Linting
flake8 server.py
mypy server.py
```

### Frontend Scripts
```bash
# Instalar dependencias (USAR YARN)
yarn install

# Servidor de desarrollo
yarn start

# Build de producción
yarn build

# Ejecutar tests
yarn test

# Eject (no recomendado)
yarn eject
```

---

## 📊 Análisis de Dependencias

### Backend - Tamaño y Propósito

| Dependencia | Tamaño | Propósito | Crítica |
|-------------|--------|-----------|---------|
| fastapi | ~15MB | Framework web | ⭐⭐⭐ |
| motor | ~8MB | MongoDB async | ⭐⭐⭐ |
| pydantic | ~12MB | Validación | ⭐⭐⭐ |
| python-jose | ~5MB | JWT tokens | ⭐⭐⭐ |
| passlib | ~3MB | Password hashing | ⭐⭐⭐ |
| uvicorn | ~6MB | ASGI server | ⭐⭐⭐ |

### Frontend - Bundle Analysis

| Categoría | Dependencias | Propósito | Bundle Impact |
|-----------|-------------|-----------|---------------|
| React Core | 3 | Framework | ~150KB |
| Radix UI | 25+ | Componentes | ~300KB |
| Routing | 1 | Navegación | ~50KB |
| HTTP | 1 | API calls | ~30KB |
| Icons | 1 | Iconografía | ~100KB |
| Utils | 8 | Utilidades | ~200KB |

---

## 🚨 Dependencias Críticas

### No Eliminar Nunca
```txt
# Backend
fastapi              # Core framework
motor               # Database driver
pydantic            # Data validation
python-jose         # JWT authentication
passlib[bcrypt]     # Password security

# Frontend
react               # Core library
react-dom           # DOM rendering
react-router-dom    # Navigation
axios               # HTTP client
```

### Opcionales para Producción
```txt
# Backend - Development only
pytest              # Solo para testing
black               # Solo para desarrollo
flake8              # Solo para desarrollo
mypy                # Solo para desarrollo

# Frontend - Build tools
@types/*            # Solo para desarrollo TypeScript
tailwindcss         # Se compila en build
```

---

## 🔄 Actualizaciones y Compatibilidad

### Versionado Semántico

**Backend (Python)**
- **Major versions**: Requieren testing extensivo
- **Minor versions**: Generalmente seguras
- **Patch versions**: Actualizaciones de seguridad

**Frontend (Node.js)**
- **Caret (^)**: Actualizaciones compatibles automáticas
- **Tilde (~)**: Solo patches
- **Exact versions**: Para estabilidad crítica

### Comandos de Actualización

```bash
# Backend - Verificar actualizaciones disponibles
pip list --outdated

# Backend - Actualizar dependencia específica
pip install --upgrade fastapi

# Frontend - Verificar actualizaciones
yarn outdated

# Frontend - Actualizar dependencia específica
yarn upgrade react

# Frontend - Actualizar todas las dependencias
yarn upgrade
```

### Matriz de Compatibilidad

| Python Version | FastAPI | MongoDB | React Version | Node.js |
|----------------|---------|---------|---------------|---------|
| 3.11+ | ✅ 0.110.1 | ✅ 5.0+ | 19.0+ | ✅ 18+ |
| 3.10 | ✅ 0.100+ | ✅ 5.0+ | 18.0+ | ✅ 16+ |
| 3.9 | ⚠️ 0.95+ | ✅ 4.4+ | 17.0+ | ✅ 14+ |

---

## 🛡️ Seguridad de Dependencias

### Vulnerabilidades Conocidas
```bash
# Backend - Audit de seguridad
pip audit

# Frontend - Audit de seguridad
yarn audit

# Actualizar dependencias con vulnerabilidades
yarn audit fix
```

### Dependencias de Seguridad Crítica
- **bcrypt**: Hashing de contraseñas
- **cryptography**: Cifrado JWT
- **python-jose**: Tokens seguros

### Best Practices
1. **Actualizar regularmente** las dependencias de seguridad
2. **Monitorear vulnerabilidades** con herramientas automáticas
3. **Testing extensivo** después de actualizaciones
4. **Backup de versiones** funcionando antes de actualizar

---

## 📈 Performance de Dependencias

### Backend - Tiempo de Inicio
```bash
# Profiling de importaciones
python -X importtime server.py

# Dependencias más lentas al importar:
# 1. pandas (~2s)
# 2. boto3 (~1.5s)
# 3. motor (~0.5s)
```

### Frontend - Bundle Size
```bash
# Análisis de bundle
yarn build
npx source-map-explorer build/static/js/*.js

# Bibliotecas más pesadas:
# 1. Radix UI components (~300KB)
# 2. React framework (~150KB)
# 3. Lucide icons (~100KB)
```

### Optimizaciones Recomendadas

**Backend**
- **Lazy imports** para pandas y boto3
- **Uvloop** para mejor performance asyncio
- **OrJSON** para JSON más rápido

**Frontend**
- **Code splitting** por rutas
- **Lazy loading** de componentes Radix
- **Tree shaking** habilitado por defecto

---

## 🔍 Troubleshooting de Dependencias

### Errores Comunes

#### Backend
```bash
# Error: ModuleNotFoundError
pip install -r requirements.txt

# Error: bcrypt compilation failed
pip install --only-binary=all bcrypt

# Error: MongoDB connection
pip install motor[srv]  # Para MongoDB Atlas
```

#### Frontend
```bash
# Error: Module parse failed
rm -rf node_modules yarn.lock
yarn install

# Error: React version mismatch
yarn install --check-files

# Error: PostCSS plugin
yarn add --dev autoprefixer postcss
```

### Comandos de Diagnóstico
```bash
# Backend - Información del entorno
pip freeze > current_versions.txt
python --version
pip --version

# Frontend - Información del proyecto
yarn list --depth=0
node --version
yarn --version
```

---

**Documentación actualizada**: Enero 2025  
**Próxima revisión**: Cada actualización mayor de dependencias