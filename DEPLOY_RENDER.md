# TCG Hub - Deployment Guide para Render.com

## 📋 Preparación Completada

Tu aplicación ya está lista para desplegarse en Render.com con las siguientes configuraciones:

### ✅ Archivos Creados/Modificados:

1. **requirements.txt** - Dependencias actualizadas con:
   - gunicorn (servidor WSGI para producción)
   - psycopg2-binary (driver PostgreSQL)
   - python-dotenv (gestión de variables de entorno)

2. **Procfile** - Comando para iniciar la aplicación

3. **render.yaml** - Configuración automática de Render (Blueprint)

4. **.env.example** - Plantilla de variables de entorno

5. **app.py** - Modificado para:
   - Soportar PostgreSQL en producción
   - Usar variables de entorno
   - Ajustar puerto dinámicamente

---

## 🚀 Pasos para Desplegar en Render.com

### Opción A: Deploy con Blueprint (Recomendado)

1. **Sube tu código a GitHub:**
   ```bash
   cd flask_app
   git init
   git add .
   git commit -m "Preparar app para Render"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/tcghub.git
   git push -u origin main
   ```

2. **En Render.com:**
   - Ve a https://render.com y crea una cuenta
   - Click en "New +" → "Blueprint"
   - Conecta tu repositorio GitHub
   - Render detectará automáticamente `render.yaml`
   - Click en "Apply" para crear el servicio web + base de datos PostgreSQL

### Opción B: Deploy Manual

1. **Sube código a GitHub** (igual que Opción A)

2. **Crear Base de Datos PostgreSQL:**
   - En Render Dashboard → "New +" → "PostgreSQL"
   - Nombre: `tcghub-db`
   - Plan: Free
   - Copia la "Internal Database URL"

3. **Crear Web Service:**
   - "New +" → "Web Service"
   - Conecta tu repo de GitHub
   - Configuración:
     - **Name:** tcghub
     - **Region:** Oregon (o la más cercana)
     - **Branch:** main
     - **Root Directory:** (dejar vacío o poner `flask_app` si subes todo el proyecto)
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Free

4. **Agregar Variables de Entorno:**
   - En "Environment" tab del servicio:
     ```
     SECRET_KEY = [genera uno aleatorio de 50+ caracteres]
     DATABASE_URL = [pega la Internal Database URL de PostgreSQL]
     FLASK_ENV = production
     ```

5. **Deploy:**
   - Click en "Create Web Service"
   - Render compilará e iniciará tu app (toma ~5 min)

---

## ⚠️ Consideraciones Importantes

### 1. **Archivos Subidos (Imágenes)**
Los archivos en `static/uploads/` se pierden en cada redeploy. Opciones:

**Solución A - Render Disk (Persistente):**
- En tu servicio → "Settings" → "Disks"
- Añadir disco: Mount Path = `/opt/render/project/src/static/uploads`, Size = 1GB (gratis)

**Solución B - Cloudinary (Recomendado para producción):**
- Usa servicio externo de almacenamiento
- Requiere modificar el código de upload

### 2. **Base de Datos**
- PostgreSQL Free tier: 90 días gratis, luego necesitas plan paid o recrear
- Hacer backups periódicos
- Las tablas se crean automáticamente en el primer inicio

### 3. **Usuario Admin Inicial**
El usuario `admin/admin123` se crea automáticamente en el primer inicio. **Cámbialo después del primer login.**

### 4. **Dominio Personalizado**
- Render da un dominio: `https://tcghub-XXXX.onrender.com`
- Puedes conectar tu dominio propio en Settings → Custom Domains

### 5. **Plan Free Limitations**
- App "duerme" tras 15 min sin actividad
- Primera carga después de dormir toma ~30 seg
- 750 horas/mes gratis (suficiente para 1 servicio 24/7)

---

## 🔍 Verificación Post-Deploy

1. Visita tu URL de Render
2. Verifica que cargue la página principal
3. Ve a `/admin` e inicia sesión
4. Prueba crear un torneo
5. Sube un logo y verifica que se muestre
6. Activa el popup y verifica que aparezca

---

## 🐛 Troubleshooting

**Error: "Application failed to respond"**
- Revisa logs en Render Dashboard → tu servicio → Logs
- Verifica que DATABASE_URL esté correctamente configurada

**Imágenes no se muestran:**
- Configura Render Disk (ver sección "Archivos Subidos")
- O usa Cloudinary para almacenamiento externo

**Base de datos vacía:**
- Las tablas se crean automáticamente
- Usuario admin se crea en primer inicio
- Revisa logs para ver mensajes de inicialización

---

## 📞 Próximos Pasos

1. Deploy en Render siguiendo Opción A o B
2. Cambiar contraseña de admin
3. Configurar disco persistente o Cloudinary
4. (Opcional) Conectar dominio personalizado
5. (Opcional) Configurar GitHub Actions para auto-deploy

¿Necesitas ayuda con algún paso específico?
