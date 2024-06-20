# Buho Monitor

```markdown

Este proyecto monitorea múltiples archivos de log y envía actualizaciones en tiempo real a través de WebSockets utilizando Django Channels y Redis.

## Requisitos

- Python 3.12
- Django 4.x
- Redis
- Django Channels
- Watchdog

## Instalación

Sigue los pasos a continuación para configurar el proyecto en un ambiente Linux.

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu_usuario/log_monitor.git
cd log_monitor
```

### 2. Configurar el Entorno Virtual

Crea un entorno virtual para el proyecto:

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

Instala las dependencias necesarias usando pip:

```bash
pip install -r requirements.txt
```

Asegúrate de que el archivo `requirements.txt` contenga las siguientes dependencias:

```
Django==4.x
channels==4.x
channels_redis==4.x
watchdog==3.x
```

### 4. Configurar Redis

Instala Redis en tu sistema. En Ubuntu, puedes usar el siguiente comando:

```bash
sudo apt-get update
sudo apt-get install redis-server
```

Inicia el servicio de Redis:

```bash
sudo systemctl start redis-server
```

### 5. Configurar Django

Crea un archivo `.env` en el directorio del proyecto y configura las variables de entorno necesarias:

```env
DJANGO_SETTINGS_MODULE=buhomonitor.settings
```

### 6. Configurar settings.py

En tu archivo `settings.py`, agrega la configuración de Django Channels y Redis:

```python
INSTALLED_APPS = [
    ...
    'channels',
    ...
]

ASGI_APPLICATION = 'buhomonitor.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```

### 7. Ejecutar Migraciones

Ejecuta las migraciones de Django para preparar la base de datos:

```bash
python manage.py migrate
```

### 8. Ejecutar el Servidor de Desarrollo

Inicia el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

### 9. Ejecutar el Monitor de Logs

Ejecuta el script `log_monitor.py` para comenzar a monitorear los archivos de log:

```bash
python scripts/log_monitor.py
```

## Uso

Este proyecto monitorea los siguientes archivos de log por defecto:

- `/var/log/test_buhomonitor.log`
- `/var/log/otro_log.log`

Puedes agregar más archivos a la lista `log_file_paths` en el script `log_monitor.py`.

Las actualizaciones de los logs se envían en tiempo real a través de WebSockets y se pueden recibir en el frontend configurando un consumidor de WebSocket en Django Channels.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
```

Este archivo `README.md` proporciona las instrucciones necesarias para instalar y configurar tu proyecto de monitor de logs en un entorno Linux. Asegúrate de adaptar las partes específicas como las rutas de archivos y configuraciones según tus necesidades particulares.