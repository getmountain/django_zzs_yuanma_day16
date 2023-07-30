from rest_framework.generics import GenericAPIView

from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ViewSetMixin

from rest_framework.response import Response

from rest_framework import serializers
from api import models


class GvsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = "__all__"


class GvsView(ViewSetMixin, GenericAPIView):
    # queryset = None
    # serializer_class = GvsSerializer

    def list(self, request):
        return Response("...")

    def create(self, request):
        return Response("...")

    def retrieve(self, request, pk):
        return Response("...")
