from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CatPics
from .serializers import *
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from catagram.utils.image_utils import get_file_hash
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import OutstandingToken
from rest_framework import permissions

from .serializers import PostSerializer
from .yolo import yolotest2

from .models import Post, UserProfile
from .models import UserManager

from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework_simplejwt.views import TokenViewBase

from django.views.decorators.csrf import csrf_exempt
import json
import jwt

from django.forms.models import model_to_dict
#from .jwt_fuc import create_jwt, verify_jwt

import logging

from django.db import transaction

logger = logging.getLogger(__name__)

UserProfile = get_user_model()

class UserCreateAPIView(APIView):
    serializer_class = UserCreateSerializer
    @extend_schema(
        request=UserCreateSerializer,
        responses={   
            status.HTTP_201_CREATED: openapi.Response(description="User created"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid email or password"),
        }
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        user = UserProfile.objects.create_user(email=email, username=username, password=password)
        user.save()
        return Response({'success': 'user created'},status=status.HTTP_201_CREATED)

    def get(self, request):
        user_id = request.GET.get('user_id')
        if user_id is not None:
            # Get user by id
            try:
                # user = UserProfile.objects.get(id=user_id)
                # data = {'user': user.__dict__}
                user = UserProfile.objects.filter(id=int(user_id)).values()
                data = {'user': list(user)[0]}
            except (UserProfile.DoesNotExist, ValueError):
                data = {'error': f'User with id={user_id} does not exist'}
        else:
            # Get all users
            users = UserProfile.objects.all()
            data = {'users': list(users.values())}

        return JsonResponse(data)

class LoginApi(APIView):
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(description="Login successful"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid email or password"),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(serializer.user)
        return Response({
            'access_token': str(serializer.validated_data['access']),
            'refresh_token': str(refresh),
        })

class LogoutApi(TokenViewBase):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LogoutSerializer
    @extend_schema(
        request=LogoutSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description="Logout successful"),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid token"),
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response(status=204)
        except Exception as e:
            return Response(status=400, data={"error": "Invalid token"})

class PostApi(APIView):
    parser_classes = [MultiPartParser]
    serializer_class = PostSerializer

    @extend_schema(
        request=PostSerializer,
        responses={
            status.HTTP_201_CREATED: PostSerializer,
        },
    )
    def post(self, request):
        try:
            user = request.user
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

    def get(self, request, post_id=None, user_id=None):
        # Get all post
        if post_id and user_id is None:
            all_post = Post.objects.all()
            data = {'post': list(all_post.values())}
        else:
            if user_id is None:
                # Get post by post_id
                try:
                    user = UserProfile.objects.get(id=post_id)
                    data = {'user': user.__dict__}
                except UserProfile.DoesNotExist:
                    data = {'error': f'User with id={post_id} does not exist'}
            elif post_id is None:
                pass
            else:
                pass
        
        return JsonResponse(data)

# Test for upload catpic
class UploadCatPicApi(GenericAPIView):
    serializer_class = CatPicsSerializer
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=CatPicsSerializer,
        responses={
            status.HTTP_201_CREATED: CatPicsSerializer,
        },
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
