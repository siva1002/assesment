from rest_framework import serializers
from app.models import Friends

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Friends
        fields=('id','user','friend','request_status')

class FriendsSerializer(serializers.ModelSerializer):
    friendname=serializers.CharField(source='friend.username')
    class Meta:
        model=Friends
        fields=('friend','request_status','friendname')

class ChangeRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Friends
        fields=('request_status',)