from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("phone_number", "refer_number", "foreign_referal")
        model = User


class ReferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("phone_number",)
        model = User
