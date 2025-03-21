from rest_framework import serializers
from django.contrib.auth.hashers import check_password

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_active',
            'last_login',
            'date_joined',
        )
        read_only_fields = (
            'user_id',
            'role',
            'is_active',
            'last_login',
            'date_joined',
        )

    def to_representation(self, instance):
        # Hide sensitive information from non-admin users
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.role != 'admin':
            data.pop('user_id')
            data.pop('role')
            data.pop('is_active')
            data.pop('last_login')
            data.pop('date_joined')
        return data
    
    def update(self, instance):
        # Hide sensitive information from non-admin users
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.role != 'admin':
            data.pop('user_id')
            data.pop('role')
            data.pop('is_active')
            data.pop('last_login')
            data.pop('date_joined')
        return data

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate(self, data):
        """Validate that new_password is different from old_password"""
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({"new_password": "New password must be different from old password."})
        return data
