from rest_framework.serializers import ModelSerializer,Serializer
from rest_framework import serializers
from app.models import User

class SignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'mobile_number')
    
    def create(self, validated_data):
        user=User.objects.create(username=validated_data.get('username'), 
                                 email=validated_data.get('email'),mobile_number=validated_data.get('mobile_number'))
        user.set_password(validated_data.get('password'))
        user.save()
        return user

class LoginSerializer(Serializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(required=True)