from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('chat-query/', views.chat_query, name='chat_query'),
]
