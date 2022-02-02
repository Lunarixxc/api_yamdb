from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User

from .serializers import (UserEmailSerializer, UsersSerializer,
                          UserTokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_email_code(request):
    serializer = UserEmailSerializer(data=request.data)
    username = request.data.get('username')
    email = request.data.get('email')
    serializer.is_valid(raise_exception=True)
    users = User.objects.filter(email=email)
    try:
        if len(users) == 0:
            user = User.objects.create_user(username=username, email=email)
        elif len(users) == 1:
            user = get_object_or_404(User, username=username, email=email)
        else:
            raise IntegrityError
    except (IntegrityError, Http404):
        return Response(
            {'message': "Данный пользователь уже существует"},
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user=user)
    theme = "Код подтверждения"
    text = f'Ваш код подтверждения: {confirmation_code}'
    send_mail(
        theme, text,
        "Yamdb@yandex.ru", [email],
        fail_silently=False,
    )
    return Response(
        {'message': f"Код на почту {email} успешно отправлен"},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = UserTokenSerializer(data=request.data)
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user=user, token=confirmation_code):
        token = RefreshToken.for_user(user)
        return Response(
            {"token": str(token.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )
