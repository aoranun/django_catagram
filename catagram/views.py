from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CatPics
from .serializers import CatPicsSerializer
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from catagram.utils.image_utils import get_file_hash

from .serializers import PostSerializer
from .models import Post

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all().order_by('p_picname')
#     serializer_class = PostSerializer

class PostApi(APIView):
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('p_picname', openapi.IN_FORM, type=openapi.TYPE_STRING, description=''),
            openapi.Parameter('caption', openapi.IN_FORM, type=openapi.TYPE_STRING, description=''),
            openapi.Parameter('p_time', openapi.IN_FORM, type=openapi.TYPE_STRING, description=''),
            openapi.Parameter('like_count', openapi.IN_FORM, type=openapi.TYPE_STRING, description='')
        ],
        operation_description="Post a Cat Pictures",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Post successfully"
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input or image upload failed"
            ),
        },
        tags=["Post Cat"],
    )
    def post(self, request):
        try:
            Post(
                p_picname=request.data['p_picname'],
                caption=request.data['caption'],
                p_time=request.data['p_time'],
                like_count=request.data['like_count']
            ).save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        pass

class UploadCatPicApi(APIView):
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description=''),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description='')
        ],
        operation_description="Upload a cat picture",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Cat picture uploaded successfully"
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input or image upload failed"
            ),
        },
        tags=["Cat Pictures"],
    )
    def post(self, request):
        try:
            CatPics(
                title=get_file_hash(request.data['image']),
                image=request.data['image']
            ).save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)