from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import serializers
from api import models


class DemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"


from rest_framework.pagination import PageNumberPagination


class DemoView(GenericAPIView):
    queryset = models.UserInfo.objects.all()
    serializer_class = DemoSerializer

    # pagination_class = PageNumberPagination
    # pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, *args, **kwargs):
        # 1.数据库获取数据
        # queryset = models.UserInfo.objects.all()
        queryset = self.get_queryset()

        # 2.分页
        # from rest_framework.pagination import PageNumberPagination
        # pager = PageNumberPagination()
        # result = pager.paginate_queryset(queryset, request, self)
        result = self.paginate_queryset(queryset)

        # 3.序列化
        # ser = DemoSerializer(instance=queryset, many=True)
        # print(ser.data)
        ser = self.get_serializer(instance=result, many=True)
        # return Response("...")

        response = self.get_paginated_response(ser.data)
        return response


from rest_framework.permissions import BasePermission
from rest_framework.filters import BaseFilterBackend


class MyFilterBackend1(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # xx = request.query_params.get("xx")
        # queryset = queryset.filter(status=xx)
        return queryset


class MyFilterBackend2(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset


class DemoDetailView(GenericAPIView):
    queryset = models.UserInfo.objects

    # filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    filter_backends = [MyFilterBackend1, MyFilterBackend2]

    def get(self, request, pk):
        print(pk)  # pk=主键   id=xx

        # 1.取数据
        # obj = models.UserInfo.objects.filter(pk=pk).first()
        # obj = models.UserInfo.objects.get(id=10)   # id=10那条数据必须找到 & 必须只有一条
        # obj = models.UserInfo.objects.filter(status=2).get(id=10)   # id=10那条数据必须找到 & 必须只有一条
        # obj = models.UserInfo.objects.filter(status=请求参数xx).get(id=10)   # id=10那条数据必须找到 & 必须只有一条
        # 取数据 + 权限校验  has_object_permission
        obj = self.get_object()

        # 2.序列化
        # ser = DemoSerializer(instance=obj, many=False)
        # ser.data
        ser = self.get_serializer(instance=obj, many=True)

        return Response(ser.data)
