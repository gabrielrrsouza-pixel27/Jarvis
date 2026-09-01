from django.urls import path

from .api import chat, forget_memory, memories
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('api/chat/', chat, name='chat'),
    path('api/memories/', memories, name='memories'),
    path('api/memories/<int:memory_id>/', forget_memory, name='forget-memory'),
]
