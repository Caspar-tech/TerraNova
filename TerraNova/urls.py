from django.contrib import admin
from django.urls import path, include
from Game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Game.urls')),
    path('register/', views.register, name='register'),
]