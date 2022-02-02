from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User

from .serializers import (ConfirmationCodeSerializer, UserEmailSerializer,
                          UsersSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    # сделал username обязательным, мб нужно будет тут что-то поменять
    """API для отправки кода подтверждения на почту"""
    # request.data - это то что мы отправляем в json
    username = request.data.get('username') 
    # стандарт назначение сериалайзера
    serializer = UserEmailSerializer(data=request.data)
    # По сути тоже самое что и 
    # if not serializer.is_valid():
    #   raise ValidationError(serializer.errors)
    # Но способ написать это чище приведен ниже
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    # если username написан в запросе.
    # в общем тут идет проверка, если такой пользователь уже есть, то оно говорит что 
    # пользователь уже зарегестрирован, а если нет то создает нового.
    if username is not None:
        try:
            User.objects.create_user(username=username, email=email)
        # как я понимаю IntegrityError возникает в случаях когда есть ошибки с уникальными значениями
        # + еще возникает когда есть какое-то not null ограничение 
        except IntegrityError:
            return Response(
                {'Error': 'Пользователь с таким '
                          'username/email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
                )
    # user получает созданного выше пользователя или если
    # если пользователь ввел только email
    user = get_object_or_404(User, email=email)
    # создает для данного пользователя default_token , который отправится на почту
    # как я понимаю созданный токен прикрепляется к юзеру, позже его можно будет получить
    confirmation_code = default_token_generator.make_token(user)
    mail_subject = 'Код подтверждения'
    message = f'Ваш код подтверждения: {confirmation_code}'
    # если fail_silently - True, то он скипает все ошибки
    # fail_silently можно не ставить
    send_mail(mail_subject, message, 'Yamdb.ru <admin@yamdb.ru>',
              [email], fail_silently=False)
    return Response(
        {'Успешно': f'На почту {email} был выслан код подтверждения'},
        status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """API для получения jwt-токена"""
    serializer = ConfirmationCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)},
            status=status.HTTP_200_OK
            )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
        )
