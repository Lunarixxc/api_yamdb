from email.policy import default
from importlib.metadata import requires

from rest_framework import serializers
from reviews.models import ROLES, User


class UsersSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLES, default = ROLES[0][0])
    email = serializers.EmailField(required=True)
    
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
