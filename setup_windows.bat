@echo off
REM ═══════════════════════════════════════════════════════════
REM  setup_windows.bat — Configuración automática (Windows)
REM  Sistema Escolar Django | Python 3.12
REM ═══════════════════════════════════════════════════════════

echo.
echo  ██████████████████████████████████████████
echo   Sistema Escolar Django — Setup Windows
echo  ██████████████████████████████████████████
echo.

REM 1. Crear entorno virtual
echo [1/6] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (echo ERROR: Python 3.12 no encontrado. Instala desde python.org & pause & exit /b 1)

REM 2. Activar entorno
echo [2/6] Activando entorno virtual...
call venv\Scripts\activate.bat

REM 3. Instalar dependencias
echo [3/6] Instalando dependencias (puede tardar unos minutos)...
pip install --upgrade pip -q
pip install -r requirements.txt
if errorlevel 1 (echo ERROR al instalar dependencias & pause & exit /b 1)

REM 4. Configurar .env
if not exist .env (
    echo [4/6] Creando archivo .env desde .env.example...
    copy .env.example .env
    echo.
<<<<<<< HEAD
<<<<<<< HEAD
    echo  IMPORTANTE: Con XAMPP el DB_PASSWORD debe quedar VACIO (sin contrasena)
=======
    echo  IMPORTANTE: Edita el archivo .env con tu contrasena de MySQL
>>>>>>> 19d2c3af1c98f2eda2fa8b1aec62310d8c577731
=======
    echo  IMPORTANTE: Edita el archivo .env con tu contrasena de MySQL
>>>>>>> 19d2c3af1c98f2eda2fa8b1aec62310d8c577731
    echo  Abre .env con un editor de texto y cambia DB_PASSWORD
    echo.
    pause
) else (
    echo [4/6] Archivo .env ya existe, omitiendo...
)

REM 5. Migraciones
echo [5/6] Ejecutando migraciones...
python manage.py migrate
if errorlevel 1 (echo ERROR en migraciones. Verifica MySQL y el archivo .env & pause & exit /b 1)

REM 6. Datos de prueba
echo [6/6] Cargando datos de prueba...
python cargar_datos.py

echo.
echo  ╔════════════════════════════════════════╗
echo  ║   Instalacion completada con exito!   ║
echo  ╚════════════════════════════════════════╝
echo.
echo  Ejecuta el servidor con:
echo     venv\Scripts\activate
echo     python manage.py runserver
echo.
echo  Luego abre: http://127.0.0.1:8000
echo.
pause
