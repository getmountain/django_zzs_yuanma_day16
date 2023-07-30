from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import ModelViewSet

from rest_framework import serializers
from rest_framework.response import Response
from api import models


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = "__all__"


class BlogView(ListModelMixin, RetrieveModelMixin, GenericViewSet):  # (ViewSetMixin, generics.GenericAPIView)
    queryset = models.Blog.objects.all()
    serializer_class = BlogSerializer

    # pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get_serializer_class(self):
        # 两个请求哪里不同？GET
        pk = self.kwargs.get('pk')
        if pk:
            return self.serializer_class
        return self.serializer_class


# --------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"


# class UserView(ModelViewSet):
# class UserView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin,
#                GenericViewSet):
# api/user/
#       GET
#       POST

# api/user/yyy/123/xxx
#       GET
#       POST
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend


class MyFilterBackend1(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # request.query_params.get("xxx")
        return queryset


class MyFilterBackend2(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset


class UserView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = models.UserInfo.objects.all().order_by('-id')
    serializer_class = UserSerializer

    filter_backends = [MyFilterBackend1, MyFilterBackend2]

    @action(detail=False, methods=['get'], url_path="yyy/(?P<xx>\d+)/xxx")
    def get_password(self, request, xx, pk=None):
        print("来了")
        return Response("...")

    @action(detail=True, methods=['post', 'get'])
    def get_info(self, request, pk=None):
        print(pk)
        return Response("...")
