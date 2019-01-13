from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavDetailSerializer, UserFavSerializer, LeavingMessageSerializer, \
    AddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list 获取用户收藏列表
    retrieve 判断商品收藏
    create 创建商品收藏
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    """
    get query object on request
    """

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        print("get fav action {}".format(self.action))
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer

        return UserFavSerializer


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    list 获取用户留言
    create 添加留言
    delete 删除留言功能
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """
    收获地址
     list 获取收货地址
     create 添加收货地址
     update 修改收货地址
     delete 删除收获地址
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
