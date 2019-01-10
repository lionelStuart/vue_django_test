"""vue_django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from rest_framework.routers import DefaultRouter

import DjangoUeditor
import myapp.urls
from goods.views import GoodsListViewSet, BannerViewset, CategoryViewset, IndexCategoryViewset, HotSearchsViewset
from vue_django_test.settings import MEDIA_ROOT

router = DefaultRouter()

router.register('goods', GoodsListViewSet, base_name='goods')

# 轮播图url
router.register(r'banners', BannerViewset, base_name="banners")
# 配置category的url
router.register(r'categorys', CategoryViewset, base_name="categorys")

router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")

router.register(r'hotsearchs', HotSearchsViewset, base_name="hotsearchs")

# 首页商品系列数据
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")

goods_list = GoodsListViewSet.as_view({
    'get': 'list',
})

router.register(r'users', UserViewset, base_name="users")



urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    # path('api/', include(myapp.urls)),
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', include(router.urls)),
    ###处理url 显示路径
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]
