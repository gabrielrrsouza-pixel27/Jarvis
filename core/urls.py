from django.urls import path

from .api import chat
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('api/chat/', chat, name='chat'),
]
