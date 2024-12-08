from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['photo']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': False, 'allow_blank': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está en uso.")
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        if 'photo' in profile_data:
            user.profile.photo = profile_data['photo']
            user.profile.save()
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)

        # Validar email único al actualizar
        new_email = validated_data.get('email', None)
        if new_email and User.objects.filter(email=new_email).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Este email ya está en uso.")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if 'photo' in profile_data:
            instance.profile.photo = profile_data['photo']
            instance.profile.save()

        return instance
