#!/usr/bin/env python3
from __future__ import print_function
import os
import time
from datetime import datetime
from tqdm import tqdm

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def autenticar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and getattr(creds, "expired", False) and getattr(creds, "refresh_token", None):
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def buscar_o_crear_carpeta(nombre_carpeta, service):
    query = f"name='{nombre_carpeta}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    resultados = service.files().list(q=query, fields="files(id, name)", spaces='drive').execute()
    archivos = resultados.get('files', [])
    if archivos:
        return archivos[0]['id']
    else:
        carpeta = {'name': nombre_carpeta, 'mimeType': 'application/vnd.google-apps.folder'}
        res = service.files().create(body=carpeta, fields='id').execute()
        return res.get('id')

def subir_a_drive(ruta_archivo):
    print("Iniciando autenticación...")
    creds = autenticar()
    print("Autenticación exitosa.")

    service = build('drive', 'v3', credentials=creds, cache_discovery=False)

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No existe el archivo: {ruta_archivo}")

    nombre_archivo = os.path.basename(ruta_archivo)
    tam = os.path.getsize(ruta_archivo)
    print(f"Subiendo: {nombre_archivo} ({tam/1024/1024:.2f} MiB)")

    carpeta_id = buscar_o_crear_carpeta('Backups', service)

    media = MediaFileUpload(
        ruta_archivo,
        mimetype='application/gzip',
        chunksize=1 * 1024 * 1024,
        resumable=True
    )

    metadata = {'name': nombre_archivo, 'parents': [carpeta_id]}

    def iniciar_sesion():
        return service.files().create(body=metadata, media_body=media, fields='id')

    intentos_sesion = 0
    max_sesiones = 3
    while True:
        try:
            request = iniciar_sesion()
            response = None
            with tqdm(total=tam, unit='B', unit_scale=True, desc="Subiendo", ncols=80) as pbar:
                bytes_subidos = 0
                while response is None:
                    status, response = request.next_chunk(num_retries=5)
                    if status:
                        nuevos_bytes = int(status.progress() * tam) - bytes_subidos
                        if nuevos_bytes > 0:
                            pbar.update(nuevos_bytes)
                            bytes_subidos += nuevos_bytes

            print(f"\nBackup subido. ID: {response.get('id')}")
            break
        except HttpError as e:
            print(f"Error HTTP de la API: {e}")
            raise
        except Exception as e:
            if "RedirectMissingLocation" in str(e) and intentos_sesion < max_sesiones:
                intentos_sesion += 1
                print("Redirección inválida detectada. Re-iniciando sesión de subida...")
                time.sleep(2)
                continue
            print(f"Error durante la subida: {e}")
            raise

if __name__ == "__main__":
    print("Iniciando proceso de backup...")
    fecha = datetime.now().strftime('%d-%m-%y')
    print(f"Fecha de backup: {fecha}")
    ruta = os.path.expanduser(f'~/backup/backup-{fecha}.tar.gz')
    print(f"Ruta del backup: {ruta}")
    print("Subiendo a Google Drive...")
    subir_a_drive(ruta)

