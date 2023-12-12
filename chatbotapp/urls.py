from django.urls import path
from django.contrib import admin
from chatbotapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bot_response/', views.bot_response, name='bot_response'),
]
