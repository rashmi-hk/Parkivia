from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """

    class Meta:
        model = CustomUser
        fields = "__all__"

