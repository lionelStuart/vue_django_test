import time

from rest_framework import serializers

from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderGoods, OrderInfo
from utils.alipay import AliPay
from vue_django_test.settings import private_key_path, ali_pub_key_path, APP_ID


class ShopCartDetailSerializer(serializers.ModelSerializer):
    """
    list 时调用 显示购物车列表
    """
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('goods', 'nums')


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车序列化 create update destory retrive
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, label=u'数量', min_value=1,
                                    error_messages={
                                        'min_value': u'商品不少于1',
                                        'required': u'选择购买数量',
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        """
        购物车中商品增加
        :param validated_data:
        :return:
        """
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        """
        购物车中商品刷新
        :param instance:
        :param validated_data:
        :return:
        """
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    单个商品的order
    """
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)


    def get_alipay_url(self, obj):
        print('order detail serializer get alipay url')

        alipay = AliPay(
            appid=APP_ID,
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        print('do direct pay')

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    # 字段 通过 get_XX 方法获取
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        print('order serializer get alipay url')
        alipay = AliPay(
            appid=APP_ID,
            app_notify_url="http://127.0.0.1:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        print('return url   {}'.format(re_url))

        return re_url

    def generate_order_sn(self):
        # 当前时间+userid+随机数
        print('gen order sn')
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}" \
            .format(time_str=time.strftime("%Y%m%d%H%M%S"),
                    userid=self.context["request"].user.id, ranstr=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        """
         on validata create order sn
        :param attrs:
        :return:
        """
        print('do validate')
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'
