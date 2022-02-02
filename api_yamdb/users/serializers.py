from rest_framework import serializers
from reviews.models import ROLES, USER, User


class UsersSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES, default = USER)
    email = serializers.EmailField(required=True)
    
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class UserEmailSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
