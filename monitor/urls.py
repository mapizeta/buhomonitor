from django.urls import path
from .views import view_logs

urlpatterns = [
    path('logs/', view_logs, name='view_logs'),
]
