from rest_framework import serializers
from reviews.models import ROLES, USER, User


class UsersSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES, default = USER)
    email = serializers.EmailField(required=True)
    
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

