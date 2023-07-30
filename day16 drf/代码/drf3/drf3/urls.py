"""drf3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from api.views import demo
from api.views import gvs
from api.views import five
from api.views import ft
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api/user', five.UserView)
router.register(r'api/ft', ft.FtView)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/demo/', demo.DemoView.as_view()),
    path('api/demo/<int:pk>/', demo.DemoDetailView.as_view()),

    path('api/gvs/', gvs.GvsView.as_view({'get': 'list', "post": "create"})),
    path('api/gvs/<int:pk>/', gvs.GvsView.as_view({'get': 'retrieve'})),

    path('api/blog/', five.BlogView.as_view({'get': 'list'})),
    path('api/blog/<int:pk>/', five.BlogView.as_view({'get': 'retrieve'})),

    # path('api/user/', five.UserView.as_view({'get': 'list', "post": "create"})),
    # path('api/user/<int:pk>/',five.UserView.as_view({'get': 'retrieve', "put": "update", "patch": "partial_update", "delete": "destroy"})),
]

urlpatterns += router.urls
