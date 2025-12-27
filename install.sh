#!/bin/bash
echo "=== Hyp-GUI Installer ==="

# Detectar sistema operativo
OS=$(uname)
if [[ "$OS" == "Linux" || "$OS" == "Darwin"  ]]; then
    echo "[OK] Compatible System: $OS"
else
    echo "[ERROR] Unsupported System"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

echo "Installing dependencies..."
if [[ ! -f "requirements.txt" ]]; then
    echo "[ERROR] requirements.txt not found!"
    exit 1
fi
pip install -r requirements.txt
