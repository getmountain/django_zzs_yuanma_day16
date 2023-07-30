import uuid
from django.shortcuts import render, HttpResponse
from api import models
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import exceptions
from ext.auth import BlogAuthentication, NoAuthentication
from ext.hook import NbHookSerializer


class BlogUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ["id", "username"]


class BlogSerializers(NbHookSerializer, serializers.ModelSerializer):
    ctime = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    creator = BlogUserSerializers(read_only=True)

    class Meta:
        model = models.Blog
        fields = ['id', "category", "image", "title", "text", "summary", "ctime", "comment_count", "favor_count",
                  "creator"]
        extra_kwargs = {
            "comment_count": {"read_only": True},
            "favor_count": {"read_only": True},
            "text": {"write_only": True},
        }

    def nb_category(self, obj):
        return obj.get_category_display()


class BlogView(APIView):
    authentication_classes = [BlogAuthentication, ]

    def get(self, request, *args, **kwargs):
        """ 博客列表 """

        # 1.读取数据库中的博客信息
        queryset = models.Blog.objects.all().order_by("-id")

        # ?max_id=1
        # ?min_id=13
        max_id = request.query_params.get("max_id")
        if max_id:
            queryset = queryset.filter(id__lt=max_id)

        # 2.分页处理得到分页后的->queryset
        from rest_framework.pagination import LimitOffsetPagination

        pager = LimitOffsetPagination()
        result = pager.paginate_queryset(queryset, request, self)

        # 3.序列化
        ser = BlogSerializers(instance=result, many=True)

        # 4.获取序列化结果 or 分页返回处理
        response = pager.get_paginated_response(ser.data)
        return response

    def post(self, request):
        if not request.user:
            return Response({"code": 3000, 'error': "认证失败"})
        ser = BlogSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1002, 'error': "校验失败", 'detail': ser.errors})

        ser.save(creator=request.user)
        return Response({"code": 1000, "data": ser.data})


class BlogDetailSerializers(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_display")
    ctime = serializers.DateTimeField(format="%Y-%m-%d")
    creator = BlogUserSerializers()

    comments = serializers.SerializerMethodField()

    class Meta:
        model = models.Blog
        fields = "__all__"


class BlogDetailView(APIView):
    def get(self, request, *args, **kwargs):
        """ 博客详细 """
        # 1.获取ID
        pk = kwargs.get("pk")

        # 2.根据ID获取对象
        instance = models.Blog.objects.filter(id=pk).first()
        if not instance:
            return Response({"code": 1001, 'error': "不存在"})

        # 2.序列化
        ser = BlogDetailSerializers(instance=instance, many=False)

        # 3.返回
        context = {"code": 1000, 'data': ser.data}
        return Response(context)


class CommentSerializers(NbHookSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["id", "content", "user"]
        extra_kwargs = {
            "id": {'read_only': True},
            "user": {'read_only': True}
        }

    def nb_user(self, obj):
        return obj.user.username


class CommentView(APIView):
    authentication_classes = [BlogAuthentication, ]

    def get(self, request, blog_id):
        """ 评论列表 """
        # 1.获取评论对象
        queryset = models.Comment.objects.filter(blog_id=blog_id)

        # 2.序列化
        ser = CommentSerializers(instance=queryset, many=True)

        # 3.返回
        context = {"code": 1000, 'data': ser.data}
        return Response(context)

    def post(self, request, blog_id):
        """ 发布评论 """
        if not request.user:
            return Response({"code": 3000, 'error': "认证失败"})

        blog_object = models.Blog.objects.filter(id=blog_id).first()
        if not blog_object:
            return Response({"code": 2000, 'error': "博客不存在"})

        ser = CommentSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"code": 10002, 'error': "博客不存在", "detail": ser.errors})

        ser.save(blog=blog_object, user=request.user)
        return Response({"code": 1000, 'data': ser.data})


class RegisterSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["id", "username", "password", "confirm_password"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True}
        }

    def validate_password(self, value):
        # print("密码：", value)
        return value

    def validate_confirm_password(self, value):
        # print("重复密码", value)
        password = self.initial_data.get("password")
        if password != value:
            raise exceptions.ValidationError("密码不一致")
        return value


class RegisterView(APIView):

    def post(self, request):
        # 1.提交数据  {"username":123123,"password":123123,"confirm_password":"xxx"}

        # 2.校验 + 保存
        ser = RegisterSerializers(data=request.data)
        if ser.is_valid():
            ser.validated_data.pop("confirm_password")
            ser.save()
            return Response({"code": 1000, "data": ser.data})
        else:
            return Response({"code": 1001, 'error': "注册失败", "detail": ser.errors})


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ["username", "password"]


class LoginView(APIView):

    def post(self, request):
        # request.data  # {"username":"","password":''}
        ser = LoginSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1001, 'error': "校验失败", "detail": ser.errors})

        instance = models.UserInfo.objects.filter(**ser.validated_data).first()
        if not instance:
            return Response({"code": 1002, 'error': "用户名或密码错误"})

        token = str(uuid.uuid4())
        instance.token = token
        instance.save()

        return Response({"code": 1000, 'token': token})


class FavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favor
        fields = ["id", "blog"]


class FavorView(APIView):
    authentication_classes = [BlogAuthentication, NoAuthentication]

    def post(self, request):
        print(request.user)
        ser = FavorSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1002, 'error': "加盐失败", "detail": ser.errors})

        # 1.存在，不攒
        exists = models.Favor.objects.filter(user=request.user, **ser.validated_data).exists()
        if exists:
            return Response({"code": 1005, 'error': "已存在"})

        # 2.不存在，赞
        ser.save(user=request.user)
        return Response({"code": 1000, 'data': ser.data})


def db(request):
    # v1 = models.UserInfo.objects.create(username="wupeiqi", password='123')
    # v2 = models.UserInfo.objects.create(username="cxr", password='123')
    #
    # models.Blog.objects.create(
    #     category=1,
    #     image="xxxx/xxxxx.png",
    #     title="郑经理",
    #     summary="....",
    #     text="卡封建时代；if可结案时；了多开几份；埃里克森的机房",
    #     creator=v1
    # )
    #
    # models.Blog.objects.create(
    #     category=2,
    #     image="xxxx/xxxxx.png",
    #     title="震惊了",
    #     summary="....",
    #     text="卡封成型如居然塌方了房",
    #     creator=v2
    # )
    # models.Comment.objects.create(content='x1asdf',blog_id=1,user_id=1)
    # models.Comment.objects.create(content='x1ffff',blog_id=1,user_id=2)

    return HttpResponse("成功")
