from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, get_email_code, get_jwt_token
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet)
v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)

v1_auth_patterns = [
    path('signup/', get_email_code),
    path('token/', get_jwt_token)
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
    path('v1/', include(v1_router.urls)),
]
