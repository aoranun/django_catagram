from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

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
from .yolo import testyolov5
from .models import *
from .serializers import *
# from catagram.utils.image_utils import cat_detec_path

from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.permissions import IsAuthenticated

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

        # Check if username or email already exist
        if UserProfile.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if UserProfile.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = UserProfile.objects.create_user(email=email, username=username, password=password)
        user.save()
        return Response({'success': 'user created'},status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwarqs):
        # Get user by id
        user_id = request.GET.get('user_id')
        if user_id is not None:
            # user id
            try:
                user = UserProfile.objects.filter(id=int(user_id)).values()
                data = {'user': list(user)[0]}
            except (UserProfile.DoesNotExist, ValueError):
                data = {'error': f'User with id={user_id} does not exist'}
        else:
            # id (from access token)
            user_id = request.user.id
            user = UserProfile.objects.filter(id=int(user_id)).values()
            data = {'users': list(user)[0]}

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
        # Get access token
        try: 
            serializer = TokenObtainPairSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh = RefreshToken.for_user(serializer.user)
            return Response({
                'access_token': str(serializer.validated_data['access']),
                'refresh_token': str(refresh),
            })
        except Exception as e:
            print(e)
            return Response(status=400, data={"error": "Invalid email or password"}) 

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
        
class LoginStatus(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        data = {
            'is_logged_in': True,
            'username': user.username,
            'email': user.email
        }
        return Response(data, status=status.HTTP_200_OK)

class TokenRefresh(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = str(refresh_token.access_token)
        except Exception as e:
            return Response({'error': 'Failed to refresh access token.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'access_token': access_token}, status=status.HTTP_200_OK)

def delete_file(filepath):
    # Delete file
    if os.path.exists(filepath):
        os.remove(filepath)

class CatDetectorAPIView(APIView):
    """
    Cat detector API
    Check if this is a picture of a cat or not.
    """
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        file = request.data['image']
        hash_file = get_file_hash(file)
        fs = FileSystemStorage()
        filename = fs.save('cat_pic/' + hash_file + '.jpg', file)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        cat_path = 'cat_pic/' + hash_file + '.jpg'
        catornot = yolotest2.yolodetect(cat_path)
        typcat = testyolov5.modelcat(cat_path)
        if catornot == 'cat':
            delete_file(cat_path)
            return Response({'message': 'This is a cat', 'type' : typcat}, status=status.HTTP_201_CREATED)
        else:
            delete_file(cat_path)
            return Response({'error': 'This picture is not a cat, please change!'}, status=status.HTTP_400_BAD_REQUEST)
    
class PostApi(APIView):
    """
    Post cat picture API
    """
    parser_classes = [MultiPartParser]
    serializer_class = PostSerializer

    @extend_schema(
        request=PostSerializer,
        responses={
            status.HTTP_201_CREATED: PostSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        # Create a new post
        user = request.user
        print(user.id)
        catpic = CatPics.objects.create_catpic(
            title=get_file_hash(request.data['image']),
            image=request.data['image']
        )
        # Create a new post
        Post.objects.create(
            caption=request.data['caption'],
            catpic=catpic,
            user_id=user.id
        ).save()
        return Response({'message':'is a cat. Created post success'},status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        post_id = request.GET.get('post_id')
        if (post_id is not None) or (user_id is not None):
            # Get all post
            print(post_id,user_id)
            if (user_id is not None) and (post_id is None):
                # Get post by user_id
                try:
                    post = Post.objects.filter(user_id=user_id)
                    data = {'post': list(post.values())}
                except Post.DoesNotExist:
                    data = {'error': f'Post with id={user_id} does not exist'}
            elif (post_id is not None) and (user_id is None):
                # Get post by post_id
                try:
                    post = Post.objects.filter(id=post_id)
                    data = {'post': list(post.values())}
                except Post.DoesNotExist:
                    data = {'error': f'Post with id={post_id} does not exist'}
            else:
                try:
                    post = Post.objects.filter(id=post_id,user_id=user_id)
                    data = {'post': list(post.values())}
                except Post.DoesNotExist:
                    data = {'error': f'User with id={post_id} does not exist'}
        else:
            print(user_id,post_id)
            all_post = Post.objects.all()
            data = {'post': list(all_post.values())}
        
        return JsonResponse(data)
    
class CommentApi(APIView):
    """
    Comment on a post API
    """
    serializer_class = CommentSerializer

    @extend_schema(
        request=CommentSerializer,
        responses={
            status.HTTP_201_CREATED: CommentSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        # Create a new comment
        try:
            user = request.user
            CommentPost.objects.create(
                    comment_text=request.data['comment_text'],
                    post_id=request.data['post_id'],
                    user_id=user.id
            ).save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        # Get all comment
        post_id = request.GET.get('post_id')
        try:
            comments = CommentPost.objects.filter(post_id=post_id)
            data = {'comments': list(comments.values())}
            return Response(data,status=status.HTTP_200_OK)
        except (CommentPost.DoesNotExist, ValueError):
            data = {'error': f'Comment with id={post_id} does not exist'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

class UploadCatPicApi(GenericAPIView):
    """
    For test upload a cat picture
    """
    serializer_class = CatPicsSerializer
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=CatPicsSerializer,
        responses={
            status.HTTP_201_CREATED: CatPicsSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        file = request.data['image']
        hash_file = get_file_hash(file)
        fs = FileSystemStorage()
        filename = fs.save('cat_pic/' + hash_file+'.jpg', file)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        catornot = yolotest2.yolodetect('cat_pic/' + hash_file + '.jpg')
        print(catornot)
        if catornot == 'cat':
            return Response({'message':'is a cat. Created post success'},status=status.HTTP_201_CREATED)
        else:
            delete_file('cat_pic/' + hash_file + '.jpg')
            return Response({'message':'is not a cat.'},status=status.HTTP_400_BAD_REQUEST)

def get_post_by_uid(user_id):
    post = Post.objects.filter(user_id=user_id)
    return post

def get_comment_by_pid(post_id):
    commet = CommentPost.objects.filter(post_id=post_id)
    return commet

def get_user_by_uid(user_id):
    user = UserProfile.objects.filter(id=user_id)
    return user

class ProfilePage(APIView):
    """
    Profile page API
    """
    serializer_class = ProfilePageSerializer
    @extend_schema(
        request=ProfilePageSerializer,
        responses={
            status.HTTP_200_OK: ProfilePageSerializer,
            status.HTTP_400_BAD_REQUEST: ProfilePageSerializer
            },
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        post = get_post_by_uid(user.id)
        data = {'user': list(user.values()),
                'post': list(post.values())}
        return JsonResponse(data)
    
    def post(self, request, *args, **kwargs):
        # Edit user profile
        pass

class HomePage(APIView):
    """
    Home page API
    """
    def get(self, request):
        post = Post.objects.all()
        catpic = CatPics.objects.filter(post.id)
        data = {'post': list(post.values() + catpic.values())}
        return JsonResponse(data)