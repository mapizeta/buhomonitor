####Ejecución de log_monitor.py
#El script log_monitor.py debe ejecutarse de manera independiente. 
# Puedes utilizar un administrador de procesos como systemd, supervisord o simplemente ejecutarlo en segundo plano usando nohup o tmux.
#
##Ejecución Manual
#python scripts/log_monitor.py
#Si deseas ejecutar el script en segundo plano y asegurarte de que continúe funcionando incluso si cierras la terminal, puedes usar nohup:
#nohup python scripts/log_monitor.py &
#
##Uso de supervisord
#supervisord es una herramienta para gestionar procesos y asegurarse de que se reinicien si fallan. 
# Aquí hay una configuración básica para supervisord:
#sudo apt-get install supervisor
#[program:log_monitor]
#command=/usr/bin/python /ruta/a/tu/proyecto/scripts/log_monitor.py
#autostart=true
#autorestart=true
#stderr_logfile=/var/log/log_monitor.err.log
#stdout_logfile=/var/log/log_monitor.out.log
#Guarda este archivo en /etc/supervisor/conf.d/log_monitor.conf.
#Recarga la configuración de supervisord y empieza a monitorear:
#sudo supervisorctl reread
#sudo supervisorctl update
#sudo supervisorctl start log_monitor

import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import datetime

# Añadir el directorio del proyecto al PYTHONPATH
sys.path.append('/home/pyzarro/Workspace/buhomonitor')

# Configurar las variables de entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buhomonitor.settings')

import django
django.setup()

class LogHandler(FileSystemEventHandler):
    def __init__(self, log_file_paths):
        self.log_file_paths = log_file_paths
        self.last_modified = {log_file: datetime.datetime.now() for log_file in log_file_paths}

    def on_modified(self, event):
        if event.src_path in self.log_file_paths:
            log_file_path = event.src_path
            current_time = datetime.datetime.now()
            time_diff = (current_time - self.last_modified[log_file_path]).total_seconds()
            if time_diff < 1:  # Ignorar modificaciones dentro de un segundo
                return
            self.last_modified[log_file_path] = current_time

            # Esperar un breve período antes de leer el archivo
            time.sleep(0.1)
            with open(log_file_path, 'r') as file:
                lines = file.readlines()
                # Envía la última línea del archivo de log a través de WebSocket
                self.send_log_update(lines[-1], log_file_path)

    def send_log_update(self, message, log_file_path):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "log_group",
            {
                "type": "log_message",
                "message": f"{log_file_path}: {message}",
            },
        )

def start_monitoring(log_file_paths):
    event_handler = LogHandler(log_file_paths)
    observer = Observer()
    for log_file_path in log_file_paths:
        observer.schedule(event_handler, path=os.path.dirname(log_file_path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Lista de archivos de log a monitorear
log_file_paths = [
    '/var/log/test_buhomonitor.log',
    '/var/log/otro_log.log'
]

start_monitoring(log_file_paths)


