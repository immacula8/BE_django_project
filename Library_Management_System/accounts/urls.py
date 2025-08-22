from django.urls import path
from .views import register_view, login_view, logout_view, subscribe_view, dashboard_view

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("subscribe/", subscribe_view, name="subscribe"),
    path('dashboard/', dashboard_view, name='dashboard'),
]
