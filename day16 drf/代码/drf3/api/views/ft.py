from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, filters

from api import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"


class MyFilterSet(FilterSet):
    min_id = filters.NumberFilter(field_name='id', lookup_expr='gte')
    us = filters.CharFilter(field_name='username', lookup_expr='startswith')

    class Meta:
        model = models.UserInfo
        fields = ["min_id", "us"]


class FtView(ListModelMixin, GenericViewSet):
    queryset = models.UserInfo.objects.all().order_by('-id')
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend, ]
    # filterset_fields = ["id", "username"]
    filterset_class = MyFilterSet
