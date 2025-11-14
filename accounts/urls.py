from . import views

from django.urls import path
from .views import CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView
from .views import RegisterView

app_name = "accounts"

urlpatterns = [
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
