from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import Register

app_name = 'users'

urlpatterns = [
    path('users', Register.as_view()),
    path('users/register', Register.as_view()),
    path('users/login', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('users/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
]
