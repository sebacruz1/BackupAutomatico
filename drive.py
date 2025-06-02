from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def autenticar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
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
        return archivos[0]['id']  # usar la primera carpeta encontrada
    else:
        return crear_carpeta(nombre_carpeta, service)

def crear_carpeta(nombre_carpeta, service):
    carpeta = {
        'name': nombre_carpeta,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    resultado = service.files().create(body=carpeta, fields='id').execute()
    return resultado.get('id')

def subir_a_drive(ruta_archivo):
    print("iniciando autenticación...")
    creds = autenticar()
    print("Autenticación exitosa.")
    service = build('drive', 'v3', credentials=creds)

    nombre_archivo = os.path.basename(ruta_archivo)
    media = MediaFileUpload(ruta_archivo, mimetype='application/gzip')
    carpeta_id = buscar_o_crear_carpeta('Backups', service)
    archivo = {
        'name': nombre_archivo,
        'parents': [carpeta_id]  
    }

    resultado = service.files().create(body=archivo, media_body=media, fields='id').execute()
    print(f"Backup subido a Google Drive. ID: {resultado.get('id')}")


print("Iniciando proceso de backup...")
fecha = datetime.now().strftime('%d-%m-%Y-%H-%M')
print(f"Fecha de backup: {fecha}")
ruta = os.path.expanduser(f'~/backup/backup-{fecha}.tar.gz')
print(f"Ruta del backup: {ruta}")
print("Subiendo a Google Drive...")
subir_a_drive(ruta)
