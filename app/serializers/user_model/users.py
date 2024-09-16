from rest_framework import serializers
from app.models import User

class UsersSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'mobile_number')