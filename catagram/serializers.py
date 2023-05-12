from rest_framework import serializers
from .models import Post
from .models import CatPics

class CatPicsSerializer(serializers.Serializer):
    image = serializers.ImageField()
    title = serializers.CharField(max_length=200)

class PostSerializer(serializers.Serializer):
    image = serializers.ImageField()
    caption = serializers.CharField(max_length=200)

class CommentSerializer(serializers.Serializer):
    comment_text = serializers.CharField(max_length=200)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    username = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class ProfilePageSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    post_id = serializers.IntegerField()
