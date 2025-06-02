#!/bin/bash

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

mkdir -p "$HOME/backup"

tar -czf "$DESTINO" "${ORIGENES[@]}"
if [ $? -eq 0 ]; then
    echo "Backup creado exitosamente en $DESTINO"
else
    echo "Error al crear el backup"
fi

cd "$HOME/backup"
ls -tp | grep 'backup-.*\.tar\.gz$' | tail -n +6 | xargs -I {} rm -- {}
