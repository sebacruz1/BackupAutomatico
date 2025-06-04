#!/bin/bash

clear
echo "-----------------------------------"
FECHA=$(date +%d-%m-%Y-%H-%M) 
ORIGENES=(
    "$HOME/.ssh"
    "$HOME/Desktop"
    "$HOME/Downloads"
    "$HOME/.zsh_history"
    "$HOME/.zshrc"
)
NOMBRE_BACKUP="backup-$FECHA.tar.gz"
DESTINO="$HOME/backup/$NOMBRE_BACKUP"
ACTUAL=$(pwd)
mkdir -p "$HOME/backup"


tar -czf "$DESTINO" "${ORIGENES[@]}"
if [ $? -eq 0 ]; then
    echo "Backup creado exitosamente en $DESTINO"
else
    echo "Error al crear el backup"
fi

cd "$HOME/backup"
ls -tp | grep 'backup-.*\.tar\.gz$' | tail -n +2 | xargs -I {} rm -- {}

source /Users/seba/Documents/BackupAutomatico/.venv/bin/activate
cd /Users/seba/Documents/BackupAutomatico || exit
python3 drive.py

if [ $? -eq 0 ]; then
    echo "Backup subido exitosamente"
    python3 sendmail.py
else
    echo "Error al subir el backup"
fi

echo "-----------------------------------"
