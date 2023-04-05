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
from django.http import JsonResponse

import logging

from django.db import transaction

logger = logging.getLogger(__name__)

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all().order_by('p_picname')
#     serializer_class = PostSerializer

class PostApi(APIView):
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description=''),
            openapi.Parameter('caption', openapi.IN_FORM, type=openapi.TYPE_STRING, description=''),
            openapi.Parameter('like_count', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='')
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
    )
    def post(self, request):
        try:
            catpic = CatPics.objects.create_catpic(
                    title=get_file_hash(request.data['image']),
                    image=request.data['image']
                )
            Post.objects.create(
                    caption=request.data['caption'],
                    like_count=request.data['like_count'],
                    catpic=catpic
                ).save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        all_post = Post.objects.all()
        data = {'post': list(all_post.values())}
        return JsonResponse(data)

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