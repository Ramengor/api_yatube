"""Модуль URL-конфигурации для приложения API."""
from django.urls import include, path, re_path

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
    re_path(r'v1/posts/(?P<post_id>\d+)/comments/$',
            CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'v1/posts/(?P<post_id>\d+)/comments/(?P<pk>\d+)/$',
            CommentViewSet.as_view(
                {'get': 'retrieve',
                 'put': 'update',
                 'patch': 'partial_update',
                 'delete': 'destroy'})
            ),
]
