from rest_framework import serializers
from .models import Post
from .models import CatPics

class CatPicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatPics
        fields = ('title', 'image')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('p_picname', 'caption', 'p_time','like_count')