# python import
import uuid

# Django imports
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from utils.enums import RequestStatus

# In house imports


# Create your models here.
class UserManger(BaseUserManager):

    def create_user(
        self, username, email, password, mobile_number=None, *args, **kwargs
    ):
        user = User.objects.create(
            username=username, email=email, mobile_number=mobile_number
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, *args, **kwargs):
        user = self.create_user(
            username=username, email=email, password=password, *args, **kwargs
        )
        user.is_superuser = True
        user.is_staff = True

        user.save()
        return user


class User(AbstractUser, AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(blank=True, null=True,max_length=40)
    nick_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table ='user'
    @property

    def owner(self):
        return self
    
    USERNAME_FIELD = "email"
    objects = UserManger()
    REQUIRED_FIELDS = ["username"]    
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}-{self.id}"

class Friends(models.Model):
    user= models.ForeignKey(User, related_name="friends",related_query_name="friends",on_delete=models.DO_NOTHING)
    friend=models.ForeignKey(User, related_name="user_friend",related_query_name="user_friend",on_delete=models.DO_NOTHING)
    request_status=models.CharField(max_length=50,choices=RequestStatus.choices(),default=RequestStatus.Sent.value)

    def __str__(self) -> str:
        return f"{self.user.username} | {self.request_status}"