from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "user", "profile_picture", "bio"]
        read_only_fields = ["id", "user"]
