from django.urls import include, path, re_path
from rest_framework import routers

from . import views
from .views import UploadCatPicApi, PostApi, LoginApi, LogoutApi, UserCreateAPIView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()
# router.register(r'post', views.PostViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include(router.urls)),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('cat_pics/', UploadCatPicApi.as_view(), name='upload_cat_pic_api'),
    path('postcat/', PostApi.as_view(), name='post_cat_api'),
    path('signin/', LoginApi.as_view(), name='signin_api'),
    path('logout/', LogoutApi.as_view(), name='logout_api'),
    path('user/',UserCreateAPIView.as_view(),name='user_api')
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]