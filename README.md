# 🎴 InterCards TCG Hub

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Sistema de gestión y visualización de torneos para Trading Card Games (TCG)**

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [API](#-api-rest) • [Tecnologías](#-tecnologías)

</div>

---

## 📋 Descripción

InterCards TCG Hub es una aplicación web moderna diseñada para facilitar la gestión y visualización de torneos de Trading Card Games. La plataforma permite a los organizadores publicar información detallada sobre eventos de Pokemon, One Piece, Yu-Gi-Oh y Magic: The Gathering, mientras que los jugadores pueden explorar torneos disponibles con filtros intuitivos.

### ✨ Características Principales

#### Para Usuarios Públicos
- 🎯 **Exploración de Torneos**: Grid interactivo con tarjetas visuales de todos los torneos
- 🔍 **Filtros Dinámicos**: Búsqueda por fecha, ubicación y tipo de juego (sin recargar la página con HTMX)
- 📅 **Calendario Visual**: Badges que indican torneos próximos vs pasados
- 🖼️ **Imágenes Personalizadas**: Cada torneo puede tener su propia imagen o diseño por defecto
- 📱 **Diseño Responsive**: Interfaz optimizada para móviles, tablets y desktop
- 👁️ **Vista Detallada**: Información completa de cada torneo (sin necesidad de login)

#### Para Administradores
- 🔐 **Acceso Seguro**: Login protegido en ruta oculta `/admin`
- 📊 **Panel de Control**: Dashboard con estadísticas y tabla de torneos
- ✏️ **CRUD Completo**: Crear, editar y eliminar torneos con formularios validados
- 🎨 **Gestión Visual**: Carga de imágenes mediante URLs
- 🔒 **Protección de Endpoints**: API REST protegida con autenticación

---

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/intercards-tcg-hub.git
cd intercards-tcg-hub/flask_app
```

2. **Crear entorno virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Iniciar la aplicación**
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

### Primera Ejecución

Al iniciar por primera vez, la aplicación automáticamente:
- ✅ Crea la base de datos SQLite
- ✅ Genera un usuario administrador por defecto
- ✅ Crea 10 torneos de ejemplo

**Credenciales de Admin:**
- Username: `admin`
- Password: `admin123`
- URL: `http://localhost:5000/admin`

> ⚠️ **Importante**: Cambia la contraseña antes de desplegar en producción.

---

## 💡 Uso

### Navegación Pública

**Página Principal** (`/`)
- Visualiza todos los torneos en un grid responsive
- Usa los filtros superiores para buscar torneos específicos:
  - 📅 **Fecha**: Selecciona una fecha específica
  - 📍 **Ubicación**: Filtra por ciudad
  - 🎮 **TCG**: Pokemon, One Piece, Yu-Gi-Oh, Magic
- Haz clic en "Ver Detalles" para información completa del torneo

### Panel de Administración

**Acceso** (`/admin`)
1. Ingresa tus credenciales
2. Serás redirigido al panel de administración

**Panel Admin** (`/admin/panel`)
- **Estadísticas**: Total de torneos, próximos eventos, tiendas activas
- **Tabla de Torneos**: Lista completa con acciones rápidas
- **Crear Torneo**: Botón para agregar nuevos eventos
- **Editar/Eliminar**: Acciones directas desde la tabla

**Crear/Editar Torneo**

Campos del formulario:
- Nombre de Tienda
- Ubicación (ciudad)
- Hora (formato 24h)
- Fecha
- Premio (opcional)
- Tipo de Juego (Pokemon, One Piece, Yu-Gi-Oh, Magic)
- Categoría (Junior, Senior, Master)
- Tipo de Torneo (League Cup, League Challenge, Liga Casual, Liga Competitiva)
- URL de Imagen (opcional - si no se proporciona, se usa diseño por defecto)

---

## 🔌 API REST

### Endpoints Públicos

#### Obtener Todos los Torneos
```http
GET /api/torneos
```
Retorna lista de todos los torneos en formato JSON.

**Respuesta Exitosa (200):**
```json
[
  {
    "id": 1,
    "nombre_tienda": "Card Shop Madrid",
    "ubicacion": "Madrid",
    "hora": "10:00",
    "fecha": "2026-01-15",
    "premio": "$100",
    "tipo_juego": "Pokemon",
    "categoria": "Senior",
    "tipo_torneo": "League Cup",
    "imagen": "https://example.com/image.jpg"
  }
]
```

#### Filtrar Torneos (HTMX)
```http
GET /api/filtrar?filtro-fecha=2026-01-15&filtro-ubicacion=Madrid&filtro-juego=Pokemon
```
Retorna HTML renderizado de torneos filtrados.

**Parámetros:**
- `filtro-fecha` (opcional): Fecha en formato YYYY-MM-DD
- `filtro-ubicacion` (opcional): Ciudad
- `filtro-juego` (opcional): Pokemon, One Piece, Yu-Gi-Oh, Magic

### Endpoints Protegidos (Requieren Autenticación)

#### Crear Torneo
```http
POST /api/torneos
Content-Type: application/json
```

**Body:**
```json
{
  "nombre_tienda": "Card Shop Madrid",
  "ubicacion": "Madrid",
  "hora": "10:00",
  "fecha": "2026-01-15",
  "premio": "$100",
  "tipo_juego": "Pokemon",
  "categoria": "Senior",
  "tipo_torneo": "League Cup",
  "imagen": "https://example.com/image.jpg"
}
```

**Respuesta (201):**
```json
{
  "mensaje": "Torneo creado exitosamente",
  "torneo": { ... }
}
```

#### Actualizar Torneo
```http
PUT /api/torneos/<id>
Content-Type: application/json
```

**Body:** (mismo que POST, campos a actualizar)

#### Eliminar Torneo
```http
DELETE /api/torneos/<id>
```

**Respuesta (200):**
```json
{
  "mensaje": "Torneo eliminado exitosamente"
}
```

### Códigos de Error

- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: No autenticado
- `404 Not Found`: Recurso no encontrado

---

## 🛠️ Tecnologías

### Backend
- **Flask 3.0.0** - Framework web de Python
- **Flask-SQLAlchemy 3.1.1** - ORM para base de datos
- **Flask-Login 0.6.3** - Manejo de sesiones y autenticación
- **SQLite** - Base de datos embebida
- **Werkzeug** - Hashing seguro de contraseñas

### Frontend
- **Tailwind CSS** - Framework CSS utility-first
- **HTMX 1.9.10** - Interactividad sin JavaScript complejo
- **Vanilla JavaScript** - Lógica del cliente

### Características Técnicas
- 🎨 **Server-Side Rendering**: Renderizado de HTML dinámico con Jinja2
- ⚡ **HTMX**: Actualizaciones parciales de DOM sin recargar
- 🔐 **Autenticación**: Sistema robusto con Flask-Login
- 📊 **ORM**: Modelos relacionales con SQLAlchemy
- 🎯 **RESTful API**: Endpoints bien estructurados
- 📱 **Mobile-First**: Diseño responsive desde el principio

---

## 📁 Estructura del Proyecto

```
flask_app/
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias Python
├── torneos.db                  # Base de datos SQLite (generada automáticamente)
├── static/
│   └── script.js              # JavaScript del cliente
├── templates/
│   ├── index.html             # Página principal pública
│   ├── login.html             # Formulario de login
│   └── admin_panel.html       # Panel de administración
└── README.md                  # Este archivo
```

---

## 🗃️ Modelo de Datos

### Tabla: `user`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Identificador único |
| username | String(80) | Nombre de usuario único |
| password_hash | String(200) | Contraseña hasheada |

### Tabla: `torneo`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Identificador único |
| nombre_tienda | String(100) | Nombre de la tienda organizadora |
| ubicacion | String(100) | Ciudad/zona |
| hora | String(5) | Hora de inicio (HH:MM) |
| fecha | String(50) | Fecha del evento (YYYY-MM-DD) |
| premio | String(100) | Descripción del premio |
| tipo_juego | String(50) | Pokemon, One Piece, Yu-Gi-Oh, Magic |
| categoria | String(20) | Junior, Senior, Master |
| tipo_torneo | String(30) | League Cup, League Challenge, etc. |
| imagen | String(500) | URL de imagen personalizada |
| created_at | DateTime | Timestamp de creación |

---

## 🔒 Seguridad

### Implementadas
✅ Contraseñas hasheadas con Werkzeug (PBKDF2)  
✅ Protección CSRF con Flask-WTF  
✅ Sesiones seguras con SECRET_KEY  
✅ Login requerido en endpoints críticos  
✅ Validación de datos en backend  

### Recomendaciones para Producción
⚠️ Cambiar `SECRET_KEY` por una clave aleatoria segura  
⚠️ Cambiar credenciales de admin por defecto  
⚠️ Usar HTTPS en producción  
⚠️ Configurar CORS apropiadamente  
⚠️ Implementar rate limiting  
⚠️ Usar base de datos PostgreSQL/MySQL en lugar de SQLite  

---

## 🚧 Roadmap

### Versión Actual: 1.0.0
- [x] CRUD completo de torneos
- [x] Sistema de autenticación
- [x] Filtros dinámicos
- [x] Panel de administración
- [x] Soporte para imágenes personalizadas

### Próximas Versiones
- [ ] **v1.1** - Sistema de registro de jugadores
- [ ] **v1.2** - Gestión de inscripciones a torneos
- [ ] **v1.3** - Sistema de brackets/emparejamientos
- [ ] **v1.4** - Notificaciones por email
- [ ] **v1.5** - Integración con APIs de TCG (precios de cartas)
- [ ] **v2.0** - Multi-tenancy (múltiples organizadores)

---

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Changelog

### [1.0.0] - 2026-01-08

#### Added
- Sistema completo de gestión de torneos
- Autenticación de administradores
- Panel de control con estadísticas
- Filtros dinámicos con HTMX
- Soporte para imágenes personalizadas
- API REST completa
- Diseño responsive con Tailwind CSS
- Torneos dummy de ejemplo

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👥 Autor

**InterCards Team**
- Proyecto: InterCards TCG Hub
- Año: 2026

---

## 📞 Soporte

¿Problemas o preguntas? Abre un issue en GitHub o contacta al equipo de desarrollo.

---

<div align="center">

**⭐ Si te gusta este proyecto, dale una estrella en GitHub! ⭐**

Hecho con ❤️ por InterCards Team

</div>
