from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, get_email_code, get_jwt_token

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', get_email_code),
    path('v1/auth/token/', get_jwt_token),
]
