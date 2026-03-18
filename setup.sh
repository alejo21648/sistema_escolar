#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  setup.sh — Configuración automática (Linux / macOS)
#  Sistema Escolar Django | Python 3.12
# ═══════════════════════════════════════════════════════════

set -e

echo ""
echo "██████████████████████████████████████████"
echo " Sistema Escolar Django — Setup Linux/Mac "
echo "██████████████████████████████████████████"
echo ""

echo "[1/6] Creando entorno virtual..."
python3 -m venv venv

echo "[2/6] Activando entorno virtual..."
source venv/bin/activate

echo "[3/6] Instalando dependencias..."
pip install --upgrade pip -q
pip install -r requirements.txt

echo "[4/6] Configurando .env..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "  ⚠️  IMPORTANTE: Edita el archivo .env con tu contraseña de MySQL"
    echo "  Ejecuta: nano .env"
    echo ""
    read -p "  Presiona ENTER cuando hayas editado .env..."
else
    echo "  .env ya existe, omitiendo."
fi

echo "[5/6] Ejecutando migraciones..."
python manage.py migrate

echo "[6/6] Cargando datos de prueba..."
python cargar_datos.py

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   ✅ Instalación completada!            ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "  Ejecuta el servidor con:"
echo "    source venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo "  Luego abre: http://127.0.0.1:8000"
echo ""
