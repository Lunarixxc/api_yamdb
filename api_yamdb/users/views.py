from rest_framework import viewsets
from reviews.models import User

from .serializers import UsersSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
