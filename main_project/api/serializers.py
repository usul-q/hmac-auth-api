from rest_framework import serializers
from .models import CustomUser

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'date_joined',
            'public_key',
            'secret'
        ]
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
            'secret': {'write_only': True},
        }

    def create(self, validated_data):
        from .utils import generate_api_keys 
        public_key, private_key = generate_api_keys()

        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.public_key = public_key
        user.private_key = private_key

        user.set_password(password)
        user.save() 

        user._private_key = private_key
        return user
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if hasattr(instance, '_private_key'):
            rep['private_key'] = instance._private_key
        return rep


class PublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'date_joined']