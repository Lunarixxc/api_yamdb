from rest_framework import serializers
from reviews.models import ROLES, USER, User


class UsersSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES, default = USER)
    email = serializers.EmailField(required=True)
    
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    # def validate_email(self, value):
    #     lower_email = value.lower()
    #     if User.objects.filter(email__iexact=lower_email).exists():
    #         raise serializers.ValidationError("Такая почта уже существует")
    #     return lower_email

class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
