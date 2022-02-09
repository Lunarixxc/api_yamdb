from rest_framework import serializers

from reviews.models import ROLES, USER, User


class UsersSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES, default=USER)
    email = serializers.EmailField(required=True)

    def validate_username(self, value):
        lower_username = value.lower()
        if lower_username == "me":
            raise serializers.ValidationError(
                "Пользователя с таким названием назвать нельзя!"
            )
        return value

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError(
                "Пользователь с такой почтой уже существует!"
            )
        return value

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class UserMeSerializer(UsersSerializer):
    role = serializers.ChoiceField(choices=ROLES, default=USER, read_only=True)


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_username(self, value):
        lower_username = value.lower()
        if lower_username == "me":
            raise serializers.ValidationError(
                "Пользователя с таким названием назвать нельзя!"
            )
        return value


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
