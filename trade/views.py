from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins
from rest_framework.views import APIView

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车
    list 获取购物车详细
    create 加入购物车
    delete 删除购物记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShoppingCartSerializer
    lookup_field = 'goods_id'

    def perform_create(self, serializer):
        """
        加入购物车后 更新商品库存
        :param serializer:
        :return:
        """
        shop_cart = serializer.save()
        goods = shop_cart.goods
        # TODO <0
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        """
        购物车销毁时还原库存
        :param instance:
        :return:
        """
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()
        pass

    def perform_update(self, serializer):
        """
        刷新界面时更新库存
        :param serializer:
        :return:
        """
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()
        pass

    def get_serializer_class(self):
        print('shop cart action {}'.format(self.action))
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewset(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    list 获取个人订单
    retrive 获取订单详细
    delete 删除订单
    create 新增订单
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        print('oreder view action {}'.format(self.action))
        if self.action == 'retrive':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        """
        创建订单时 从购物车遍历 取出商品并销毁购物车
        :param serializer:
        :return:
        """
        print("on create order")
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order


class AliPayView(APIView):
    """
    alipay-...
    """

    pass
