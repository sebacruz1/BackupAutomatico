# 🧰 BackupAutomático (macOS)

Este proyecto contiene un script Bash y un script Python que juntos permiten:

- Comprimir automáticamente los siguientes directorios y archivos:
  - `$HOME/.ssh`
  - `$HOME/Desktop`
  - `$HOME/Downloads`
  - `$HOME/.zsh_history`
  - `$HOME/.zshrc`
- Crear un archivo `.tar.gz` con la fecha y hora actual.
- Subir ese archivo a tu cuenta de **Google Drive**, dentro de una carpeta llamada `Backups`.

---

## ⚙️ Requisitos

- macOS con Bash (o Zsh ejecutando scripts Bash)
- Python 3 instalado
- Paquetes necesarios:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

## ☁️ Configuración de Google Drive

1. Ingresa a [Google Cloud Console](https://console.cloud.google.com/welcome).
2. Crea un nuevo proyecto.
3. Activa la API de Google Drive.
4. Crea credenciales del tipo **OAuth client ID**:
   - Tipo: "Escritorio"
   - Descarga el archivo `credentials.json` y guárdalo en la misma carpeta del proyecto.
5. Ejecuta por primera vez `quickstart.py` o `subir_backup.py` para autorizar tu cuenta. Esto generará el archivo `token.json`.

**⚠️ Importante:**  
- El archivo `token.json` guarda tu sesión y no debes compartirlo.
- Si cambias los permisos (*scope*), debes eliminar `token.json` y volver a autorizar.
- !! Este proyecto requiere que cada usuario cree sus propias credenciales de Google Drive. Revisa la sección “Configuración de Google Drive” !! 

---

## 🚀 Uso

1. Ejecuta el script Bash para crear el backup:

```bash
./backup.sh
```

2. El script creará el archivo `.tar.gz` en `~/backup`.

3. Luego, subirá automáticamente ese archivo a Google Drive mediante:

```bash
python3 drive.py
```
(Esto se puede desactivar comentando/borrando la linea del 28 de backup.sh)


---
## 🕒 Automatización con cron

Puedes programar este script para que se ejecute automáticamente todos los días a las 3:00 AM con `cron`.

Abre tu crontab con:

```bash
crontab -e

0 3 * * * /Users/Ruta/Al/Script/backup.sh >> /Users/Ruta/Al/Backup/cron_backup.log 2>&1
```
---

## 📁 Estructura del repositorio

```bash
├── backup.sh            # Script que crea el archivo comprimido
├── subir_backup.py      # Script en Python que sube el archivo a Google Drive
├── credentials.json     # Tus credenciales (NO subir al repositorio)
├── token.json           # Se genera automáticamente después de autenticar
├── .gitignore           # Ignora archivos sensibles
└── README.md            # Este archivo
```

---

## ✅ Resultado

- Archivos respaldados automáticamente
- Backups organizados por fecha y hora
- Subida segura a Google Drive
- Carpetas creadas automáticamente si no existen

---

## 🛡️ Seguridad

Este proyecto **no sube archivos del sistema**, solo tu información personal y configuraciones.  
Puedes modificar qué carpetas incluir editando `ORIGENES` en `backup.sh`.

---

## 📌 Licencia

The MIT License (MIT)
Copyright © 2025 <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Fork this project to create your own MIT license that you can always link to.
