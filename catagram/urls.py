from django.urls import include, path, re_path
from rest_framework import routers
from . import views
from .views import UploadCatPicApi
from .views import PostApi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('cat_pics/', UploadCatPicApi.as_view(), name='upload_cat_pic_api'),
    path('postcat/', PostApi.as_view(), name='post_cat_api')
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]