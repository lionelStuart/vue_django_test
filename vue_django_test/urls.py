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
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from rest_framework.routers import DefaultRouter

import DjangoUeditor
import myapp.urls
from goods.views import GoodsListViewSet, BannerViewset, CategoryViewset, IndexCategoryViewset, HotSearchsViewset
from trade.views import ShoppingCartViewset, OrderViewset, AliPayView
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from users.views import UserViewset, SmsCodeViewset
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

## 用户 & 注册
router.register(r'users', UserViewset, base_name="users")

router.register(r'code', SmsCodeViewset, base_name="codes")

## 用户动作 收藏 留言 收货

router.register(r'userfavs', UserFavViewset, base_name='userfavs')
router.register(r'messages', LeavingMessageViewset, base_name='messages')
router.register('address', AddressViewset, base_name='address')

## 购物车 订单
router.register(r'shopcarts', ShoppingCartViewset, base_name='shopcarts')
router.register(r'orders', OrderViewset, base_name='orders')

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/', include(myapp.urls)),
    ## 生成文档
    ## pip install coreapi django-rest-swagger
    ## >_> cool~
    path('docs', include_docs_urls(title='docs')),

    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    path('login/', obtain_jwt_token),
    path('', include(router.urls)),
    ###处理url 显示路径
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    path('alipay/return/', AliPayView.as_view(), name="alipay"),
]
