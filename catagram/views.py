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
from .models import UserProfile
from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt

import logging

from .yolo import yolotest2

from django.db import transaction

User = get_user_model()

logger = logging.getLogger(__name__)

# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all().order_by('p_picname')
#     serializer_class = PostSerializer


class LoginApi(APIView):
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING, description=''),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, description='')
        ],
        operation_description="Sign in",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="successful"
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input username or password"
            ),
        },
    )
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                profile = None
            return Response({'message': 'Login successful', 'profile': profile})
        else:
            return Response({'message': 'Invalid credentials'})

class UserProfileList(APIView):
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING, description=''),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, description=''),
            openapi.Parameter('display_name', openapi.IN_FORM, type=openapi.TYPE_STRING, description=''),
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING, description='')
        ],
        operation_description="Create User Account",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Create User Account successfully"
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input"
            ),
        },
    )
    def post(self, request):
        data = request.data

        # Check if the email already exists
        if UserProfile.objects.filter(email=data['email']).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = UserProfile(
            email=data['email'],
            username=data['username'],
            display_name=data['display_name'],
            birth_date = data.get('birth_date', None),
            follower_count=data.get('follower_count', 0),
            following_count=data.get('following_count', 0),
            gender=data.get('gender', 'N'),
            is_active=True,
            is_admin=False,
            is_staff=True,
            password=data['password'],
        )
        user.save()
        return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)
        # if request.method == 'POST':
        #     data = json.loads(request.body.decode())
        #     username = data.get('username')
        #     password = data.get('password')
        #     email = data.get('email')
        #     if username and password and email:
        #         user = UserProfile.objects.create_user(username=username, email=email, password=password)
        #         payload = {
        #         'user_id': user.id
        #         }
        #         token = jwt.encode(payload, 'secret', algorithm='HS256')
        #         return JsonResponse({'token': token.decode()})
        #     else:
        #         return JsonResponse({'error': 'Please provide a username, password, and email'}, status=400)
        # else:
        #     return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    def get(self, request, user_id=None):
        if user_id is None:
            # Get all users
            users = UserProfile.objects.all()
            data = {'users': list(users.values())}
        else:
            # Get user by id
            try:
                user = UserProfile.objects.get(id=user_id)
                data = {'user': user.__dict__}
            except UserProfile.DoesNotExist:
                data = {'error': f'User with id={user_id} does not exist'}
        
        return JsonResponse(data)

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
            # Create a new catpic
            yolotest2.yolodetect()
            catpic = CatPics.objects.create_catpic(
                    title=get_file_hash(request.data['image']),
                    image=request.data['image']
            )
            # Create a new post
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
        # Get all post
        all_post = Post.objects.all()
        data = {'post': list(all_post.values())}
        return JsonResponse(data)

# Test for upload catpic
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