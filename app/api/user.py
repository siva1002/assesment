from django.contrib.auth import authenticate,login
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from app.models import User,Friends
from utils.enums import RequestStatus
from app.serializers import (SignUpSerializer,LoginSerializer,UsersSeralizer)
from app.serializers.friends_model import (FriendsSerializer,FriendRequestSerializer,ChangeRequestStatusSerializer)


class UserSignupView(CreateAPIView):
    serializer_class=SignUpSerializer

    def post(self, request, *args, **kwargs):
        user_details=SignUpSerializer(data=request.data)
        if not user_details.is_valid():
            return Response({"message":"Invalid details","data":user_details.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user_details.save()
        return Response({"message":"User created successfully","data":user_details.data}, status=status.HTTP_201_CREATED)

class LoginView(CreateAPIView):
    serializer_class=LoginSerializer
    def post(self, request, *args, **kwargs):
        user_details=LoginSerializer(data=request.data)
        if user_details.is_valid():
            user=authenticate(request=request,
                          email=user_details.validated_data.get('email'),
                          password=user_details.validated_data.get('password'))
            if not user:
                return Response({"message":"Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            login(user=user,request=request)
            return Response({"message":"Login successful","data":{"username":user.username}}, status=status.HTTP_200_OK)

class FindUserView(ListAPIView):
    ...
    serializer_class=UsersSeralizer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        baseQueryset=User.objects.all()
        email=self.request.query_params.get('email')
        username=self.request.query_params.get('name')
        if email:
            try:
                return baseQueryset.get(email=email)
            except User.DoesNotExist:
                return User.objects.none()
        if username:
            return baseQueryset.filter(username__icontains=username)

    def get(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if not queryset:
            return Response(data=[])
        if request.query_params.get('name'):
            paginated_queryset=self.paginate_queryset(queryset)
            users=UsersSeralizer(paginated_queryset,many=True).data
            return self.get_paginated_response(data=users)
        serializer=UsersSeralizer(queryset)
        return Response(serializer.data)

class SendRequestView(RetrieveAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=UsersSeralizer
    throttle_classes=(UserRateThrottle,)

    def get(self, request, pk, *args, **kwargs):

        if not pk == request.user.id:
            user=get_object_or_404(User, pk=pk)
            friend,created=Friends.objects.update_or_create(user=request.user,
                                                            defaults={"friend":user,
                                                                      "request_status":RequestStatus.Sent.value
                                                                      })
            if created:
                return Response({"message":"Friend request sent successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Friend request already sent"}, status=status.HTTP_409_CONFLICT)
        return Response({"message":"Give another user"})

class FriendsRequestAPI(RetrieveAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=FriendRequestSerializer
    queryset=Friends.objects.all()


    def get(self, request, *args, **kwargs):
        friend_requests=Friends.objects.filter(friend_id=request.user.id,request_status=RequestStatus.Sent.value)
        serializer=FriendRequestSerializer(friend_requests, many=True).data
        return Response(data=serializer)

class FriendsAPIView(RetrieveAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class=FriendRequestSerializer
    queryset=Friends.objects.all()

    def get(self,request):
        friends=Friends.objects.filter(user_id=request.user.id,request_status=RequestStatus.Accepted.value)
        serializer=FriendsSerializer(friends, many=True).data
        return Response(data=serializer)

class ChangeRequestAPIView(UpdateAPIView):
    serializer_class=ChangeRequestStatusSerializer
    queryset=Friends.objects.all()
    permission_classes=(IsAuthenticated,)

    def update(self, request,pk, *args, **kwargs):
        friend_request=get_object_or_404(Friends, pk=pk)
        if not friend_request.friend.id == request.user.id:
            return Response({"message":"Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        request_data=ChangeRequestStatusSerializer(data=request.data)
        if not request_data.is_valid():
            return Response({"message":"Invalid request data","data":request_data.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        friend_request.request_status=request_data.validated_data.get('request_status')
        friend_request.save()
        return Response({"message":f"Friend request {request_data.validated_data.get('request_status')} successfully"}, status=status.HTTP_200_OK)
        

        