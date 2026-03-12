# 📖 MANUAL DE INSTALACIÓN — Sistema Escolar Django
## Python 3.12.10 | Django 4.2 | MySQL | Bootstrap 5

---

## ✅ REQUISITOS PREVIOS

Antes de comenzar, asegúrate de tener instalado:

| Herramienta | Versión mínima | Descarga |
|---|---|---|
| Python | **3.12.10** | https://www.python.org/downloads/ |
| MySQL | 8.0+ | https://dev.mysql.com/downloads/ |
| Git (opcional) | cualquiera | https://git-scm.com |

> ⚠️ Durante la instalación de Python en Windows, **marca la casilla "Add Python to PATH"**.

---

## 🗄️ PASO 1 — CREAR LA BASE DE DATOS MYSQL

Abre MySQL Workbench o la terminal de MySQL y ejecuta:

```sql
CREATE DATABASE sistema_escolar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Verifica que funciona:
```sql
SHOW DATABASES;
-- Debes ver "sistema_escolar" en la lista
```

---

## 📁 PASO 2 — EXTRAER EL PROYECTO

Descomprime el archivo ZIP descargado. Obtendrás la carpeta:
```
sistema_escolar/
```

Abre tu terminal (CMD en Windows, Terminal en Mac/Linux) y navega a esa carpeta:

```bash
# Windows:
cd C:\Users\TuNombre\Downloads\sistema_escolar

# Mac/Linux:
cd ~/Downloads/sistema_escolar
```

---

## 🐍 PASO 3 — CREAR EL ENTORNO VIRTUAL

Un entorno virtual aísla las dependencias del proyecto.

```bash
# Crear el entorno virtual
python -m venv venv
```

**Activar el entorno virtual:**

```bash
# Windows (CMD):
venv\Scripts\activate

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Mac / Linux:
source venv/bin/activate
```

✅ Sabrás que está activado porque verás `(venv)` al inicio de la línea en tu terminal.

---

## 📦 PASO 4 — INSTALAR DEPENDENCIAS

Con el entorno virtual **activado**, ejecuta:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Esto instalará:
- Django 4.2.16
- mysqlclient (conector MySQL para Python)
- Pillow (manejo de imágenes)
- python-decouple (variables de entorno)

> ⏳ Puede tardar 1-3 minutos según tu conexión a internet.

### ❗ Solución de errores comunes al instalar mysqlclient:

**Windows:** Si falla `mysqlclient`, instala primero:
- MySQL Connector C: https://dev.mysql.com/downloads/connector/c/
- O usa la versión wheel: `pip install mysqlclient --only-binary :all:`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
```

**Mac:**
```bash
brew install mysql-client pkg-config
export PKG_CONFIG_PATH="/usr/local/opt/mysql-client/lib/pkgconfig"
```

---

## ⚙️ PASO 5 — CONFIGURAR EL ARCHIVO .env

Copia el archivo de ejemplo:

```bash
# Windows:
copy .env.example .env

# Mac/Linux:
cp .env.example .env
```

Abre el archivo `.env` con cualquier editor de texto (Notepad, VS Code, etc.) y configura:

```ini
SECRET_KEY=django-insecure-cambia-esta-clave-en-produccion-xyz123abc
DEBUG=True

# ─── MySQL ───
DB_NAME=sistema_escolar
DB_USER=root
DB_PASSWORD=TU_PASSWORD_DE_MYSQL_AQUÍ    ← Cambia esto
DB_HOST=localhost
DB_PORT=3306
```

> 🔑 `DB_PASSWORD` es la contraseña que usas para entrar a MySQL.  
> Si tu MySQL no tiene contraseña, deja `DB_PASSWORD=` vacío.

---

## 🔄 PASO 6 — EJECUTAR LAS MIGRACIONES

Las migraciones crean todas las tablas en la base de datos MySQL.

```bash
python manage.py migrate
```

**Salida esperada (verás algo así):**
```
Operations to perform:
  Apply all migrations: academico, actividades, admin, asistencia, auth...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying usuarios.0001_initial... OK
  Applying academico.0001_initial... OK
  ...
  Applying cotizaciones.0001_initial... OK
```

✅ Si todas dicen `OK`, las tablas se crearon correctamente.

---

## 🌱 PASO 7 — CARGAR DATOS DE PRUEBA

Este paso crea usuarios y datos de ejemplo para probar el sistema:

```bash
python cargar_datos.py
```

**Salida esperada:**
```
🚀 Cargando datos de prueba...

  ✅ Admin: admin / admin123
  ✅ Profesores creados
  ✅ Estudiantes creados
  ✅ Acudiente creado
  ✅ Cursos: 10A, 11B
  ✅ Estudiantes inscritos en 10A
  ✅ Materias creadas
  ✅ Asignaciones creadas
  ✅ Productos de inventario creados

==================================================
✅ Datos cargados exitosamente.

👤 USUARIOS DE PRUEBA:
  Admin:      admin / admin123
  Profesor:   prof_maria / prof123
  Profesor:   prof_juan  / prof123
  Estudiante: est_ana    / est123
  Acudiente:  acud_rosa  / acud123
```

---

## 🚀 PASO 8 — INICIAR EL SERVIDOR

```bash
python manage.py runserver
```

**Salida esperada:**
```
Django version 4.2.16, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Abre tu navegador y ve a:
```
http://127.0.0.1:8000
```

---

## 🔑 USUARIOS DISPONIBLES PARA PROBAR

| Rol | Usuario | Contraseña | Acceso |
|---|---|---|---|
| Administrador | `admin` | `admin123` | Dashboard completo, usuarios, cursos, inventario |
| Profesor | `prof_maria` | `prof123` | Notas, asistencia, actividades de sus materias |
| Profesor | `prof_juan` | `prof123` | Notas, asistencia, actividades de sus materias |
| Estudiante | `est_ana` | `est123` | Ver notas, asistencia, entregar actividades |
| Acudiente | `acud_rosa` | `acud123` | Cotizaciones y productos |

---

## 🔧 COMANDOS ÚTILES DE DJANGO

```bash
# Crear un nuevo superusuario manualmente
python manage.py createsuperuser

# Generar migraciones después de cambiar modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Abrir shell interactivo de Django
python manage.py shell

# Ver todas las URL del proyecto
python manage.py show_urls   # (requiere django-extensions)

# Recolectar archivos estáticos (para producción)
python manage.py collectstatic
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### ❌ Error: "django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")"
**Causa:** MySQL no está corriendo o las credenciales en `.env` son incorrectas.  
**Solución:**
1. Verifica que MySQL esté iniciado (Services en Windows, o `sudo systemctl start mysql` en Linux).
2. Revisa `DB_USER`, `DB_PASSWORD`, `DB_HOST` en tu `.env`.
3. Prueba conectarte con: `mysql -u root -p`

---

### ❌ Error: "No module named 'MySQLdb'"
**Causa:** `mysqlclient` no se instaló correctamente.  
**Solución:**
```bash
pip install mysqlclient
# Si falla, intenta:
pip install PyMySQL
```
Y añade al final de `config/settings.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

### ❌ Error: "Table doesn't exist"
**Causa:** Las migraciones no se ejecutaron.  
**Solución:**
```bash
python manage.py migrate
```

---

### ❌ Error en PowerShell: "no se puede cargar el archivo ... Activate.ps1"
**Causa:** PowerShell bloquea scripts por política de seguridad.  
**Solución:** Ejecuta esto una vez en PowerShell como administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📂 ESTRUCTURA DEL PROYECTO

```
sistema_escolar/
├── config/                 # Configuración principal
│   ├── settings.py         # Ajustes (BD, apps, rutas)
│   └── urls.py             # URLs raíz del proyecto
├── apps/                   # Aplicaciones del sistema
│   ├── usuarios/           # Autenticación y roles
│   ├── academico/          # Cursos, materias, asignaciones
│   ├── notas/              # Registro de calificaciones
│   ├── asistencia/         # Control de asistencia
│   ├── actividades/        # Tareas y entregas
│   ├── inventario/         # Productos del colegio
│   ├── cotizaciones/       # Pedidos de acudientes
│   └── dashboard/          # Estadísticas por rol
├── templates/              # Plantillas HTML (Bootstrap 5)
├── static/                 # CSS, JS, imágenes estáticas
├── media/                  # Archivos subidos por usuarios
├── manage.py               # Comando principal de Django
├── requirements.txt        # Dependencias del proyecto
├── .env.example            # Plantilla de configuración
└── cargar_datos.py         # Script de datos de prueba
```

---

## 🎓 MÓDULOS IMPLEMENTADOS

| Módulo | Descripción |
|---|---|
| **Usuarios** | Login, roles (Admin/Profesor/Estudiante/Acudiente) |
| **Cursos** | Crear cursos, inscribir estudiantes |
| **Materias** | Gestión de materias académicas |
| **Asignaciones** | Vincular profesor + materia + curso |
| **Notas** | Registrar y ver calificaciones por período |
| **Asistencia** | Control diario por materia (P/A/T/E) |
| **Actividades** | Crear tareas, subir evidencias, calificar |
| **Inventario** | Catálogo de productos del colegio |
| **Cotizaciones** | Pedidos de acudientes con items |
| **Dashboard** | Estadísticas según el rol del usuario |

---

*Sistema Escolar Django — Desarrollado con Python 3.12.10 + Django 4.2 + MySQL + Bootstrap 5*
