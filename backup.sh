#!/bin/bash

clear
echo "-----------------------------------"

# Fecha para el nombre del backup
FECHA=$(date +%d-%m-%Y-%H-%M)

# Archivos y carpetas a respaldar
ORIGENES=(
    "$HOME/.ssh"
    "$HOME/Desktop"
    "$HOME/Downloads"
    "$HOME/.zsh_history"
    "$HOME/.zshrc"
    "$HOME/.vimrc"
)

# Nombre y destino del backup
NOMBRE_BACKUP="backup-$FECHA.tar.gz"
DESTINO="$HOME/backup/$NOMBRE_BACKUP"
mkdir -p "$HOME/backup"
DIRECTORIO="$(pwd)"

# Crear backup comprimido
tar -czf "$DESTINO" "${ORIGENES[@]}"
if [ $? -eq 0 ]; then
    echo "Backup creado exitosamente en $DESTINO"
else
    echo "Error al crear el backup"
fi

# Limpiar backups antiguos (dejar solo el más reciente)
cd "$HOME/backup" || exit
ls -tp | grep 'backup-.*\.tar\.gz$' | tail -n +2 | xargs -I {} rm -- {}

# Ruta al proyecto (asumimos que este script está dentro de BackupAutomatico)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activar entorno virtual
source "$DIRECTORIO/.venv/bin/activate"

# Ejecutar el script drive.py desde el directorio del proyecto
cd "$DIRECTORIO" || exit
python3 drive.py

if [ $? -eq 0 ]; then
    echo "Backup subido exitosamente"
    python3 sendmail.py
else
    echo "Error al subir el backup"
fi

echo "-----------------------------------"
