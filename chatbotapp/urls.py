from django.contrib import admin
from django.urls import path, include

app_name = 'chatbot'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')), # アクセス先のアプリを設定
]

# from django.urls import path
# from chatbotapp import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('bot_response/', views.bot_response, name='bot_response'),
# ]

