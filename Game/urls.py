from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
        path('', user_views.MainView.as_view(), name='main'),
        path('login/', auth_views.LoginView.as_view(template_name='Game/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(template_name='Game/logout.html'), name='logout'),
]