from rest_framework import serializers
from .models import Post
from .models import CatPics

class CatPicsSerializer(serializers.Serializer):
    image = serializers.ImageField()
    title = serializers.CharField(max_length=200)


class PostSerializer(serializers.Serializer):
    image = serializers.ImageField()
    caption = serializers.CharField(max_length=200)
    like_count = serializers.IntegerField()

class CommentSerializer(serializers.Serializer):
    comment = serializers.CharField(max_length=200)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    username = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
