from django.urls import path
from .api import (UserSignupView,LoginView,FindUserView,SendRequestView,
                  FriendsRequestAPI,FriendsAPIView,ChangeRequestAPIView)

urlpatterns=[
    path('signup/',UserSignupView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('finduser/',FindUserView.as_view(),name='finduser'),
    path('sendrequest/<int:pk>',SendRequestView.as_view(),name='sendrequest'),
    path('friend-requests/',FriendsRequestAPI.as_view(),name='friends-requests'),
    path('friends/',FriendsAPIView.as_view(),name='friends'),
    path('changerequest/<int:pk>',ChangeRequestAPIView.as_view(),name='changerequest'),
]