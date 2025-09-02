#!/bin/bash

clear

# Fecha para el nombre del backup
FECHA=$(date +%d-%m-%y)

# Archivos y carpetas a respaldar
# Aquí puedes agregar o quitar rutas según tus necesidades
ORIGENES=(
    "$HOME/.ssh"
    "$HOME/Desktop"
    "$HOME/Documents"
    "$HOME/.zsh_history"
    "$HOME/.zshrc"
    "$HOME/.vimrc"
)

# Carpetas a excluir
# Aquí puedes agregar o quitar rutas según tus necesidades
EXCLUDES=(
    "--exclude=""$HOME/Documents/Roms"
    "--exclude=""$HOME/Documents/ISOs"
)

# Nombre y destino del backup
NOMBRE_BACKUP="backup-$FECHA.tar.gz"
DESTINO="$HOME/backup/$NOMBRE_BACKUP"
mkdir -p "$HOME/backup"
DIRECTORIO="$(pwd)"

echo "-----------------------------------"


tar -czf "$DESTINO" "${EXCLUDES[@]}" "${ORIGENES[@]}"

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
