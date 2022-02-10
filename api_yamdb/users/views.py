from api.permissions import IsOnlyAdmin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User
from .serializers import (UserEmailSerializer, UserMeSerializer,
                          UsersSerializer, UserTokenSerializer)
from api_yamdb.settings import EMAIL


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsOnlyAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_serializer_class(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return UsersSerializer
        else:
            return UserMeSerializer

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        me = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                me, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_email_code(request):
    """Получение подтверждающего кода на почту."""
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    try:
        user, created = User.objects.get_or_create(
            username=username, email=email
        )
    except IntegrityError:
        return Response(
            {'message': 'Данный пользователь уже существует'},
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user=user)
    theme = 'Код подтверждения'
    text = f'Ваш код подтверждения: {confirmation_code}'
    send_mail(
        theme, text,
        EMAIL, [email],
        fail_silently=False,
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Получение токена с помощью подверждающего кода."""
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user=user, token=confirmation_code):
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )
