import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from catagram.utils.image_utils import catpic_image_path

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, null=False)
    username = models.CharField(max_length=30, unique=True, null=False)
    display_name = models.CharField(max_length=50, null=False)
    birth_date = models.DateField(blank=True, null=True)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    GENDER_CHOICES = [
        ('M', 'man'),
        ('W', 'woman'),
        ('N', 'not specified'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='N',
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    password = models.CharField(max_length=128, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_staff
    
    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value
        
class CatPicsManager(models.Manager):
    def create_catpic(self, title, image):
        catpic = self.create(title=title, image=image)
        return catpic
    
class CatPics(models.Model):        
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=catpic_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = CatPicsManager()

class Post(models.Model):
    #p_picname = models.CharField(max_length=200)
    caption = models.CharField(max_length=200)
    p_time = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField()
    post_at = models.DateTimeField(auto_now_add=True)
    catpic = models.OneToOneField(CatPics, on_delete=models.CASCADE)
    #user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=None)

class Board(models.Model):
    pass

    