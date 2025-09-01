from django.urls import path
from .views import register_view, login_view, logout_view, subscribe_view, dashboard_view
from . import views
from .api_views import RegisterAPIView, ProfileAPIView, SubscriptionAPIView, LoginAPIView
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("subscribe/", subscribe_view, name="subscribe"),
    path('dashboard/', dashboard_view, name='dashboard'),
    path("upgrade/<str:plan>/", views.upgrade, name="upgrade"),
    path("api/register/", RegisterAPIView.as_view(), name="api-register"),
    path("api/profile/", ProfileAPIView.as_view(), name="api-profile"),
    path("api/subscription/", SubscriptionAPIView.as_view(), name="api-subscription"),
    path("api/login/", LoginAPIView.as_view(), name="api-login"),
    path("api/token-auth/", obtain_auth_token, name="api_token_auth"),
    path("comments/", views.comments_list, name="comments"),
    path("comments/add/", views.add_comment, name="add_comment"),
    path("comments/reply/<int:pk>/", views.reply_comment, name="reply_comment"),
    path("subscription/", views.subscription_detail, name="subscription_detail"),
    path("signup/", views.register_view, name="signup"),


]
