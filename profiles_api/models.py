from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

# Create your models here.
class UserProfileManager(BaseUserManager):
    """ manager for user profiles """
    def create_user(self,email,name,password=None):
        """" create a new user profile """
        if not email:
            raise ValueError("Please provide email")
        # normalizing Email
        email =  self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        """create and save new user """
        user = self.create_user(email,name,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """ Database models for user in system """
    email = models.EmailField(max_length=255 , unique=True)
    name =models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ retreive full name of user"""
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        """ return email of user """
        return self.email

class ProfileFeedItem(models.Model):
    """ allow user to store status update in the system. everytime they create new update its gonna create new
    profile feed item object and associate that object with user using foreign key so that u will not create
    profile feed for users that is not ezits"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True) #everytime we create profilefeeditems it automatically add datatime feild
    def __str__(self):
        """ return model as a string """
        self.status_text

