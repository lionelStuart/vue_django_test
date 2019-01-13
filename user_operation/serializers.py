from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from .models import UserFav, UserAddress, UserLeavingMessage


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class UserFavSerializer(serializers.ModelSerializer):
    ## HiddenField
    # 不依靠输入， 需要设置默认的值 ，不依靠用户post 数据，不显示返回给用户 如:user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    ##校验逻辑
    # 1.独立校验 def validate_XX(self,XX):raise exception or return field
    # 2.联合校验 def validate(self,attrs): if attrs[xx] raise or return attrs
    # 3.validators 直接作用于字段 etc.
    #   3.1 serializers.XXField(... , validators=[UniqueValidators(...)]
    #   3.2 validators = [UniqueTogetherValidator(...,fields =[_1,_2...]
    ## 自带验证器
    # 1.UniqueValidator
    # 2.UniqueTogetherValidator
    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已收藏',
            )
        ]
        fields = ('user', 'goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        fields = ("id", "user", "province", "city", "district", "address", "signer_name", "add_time", "signer_mobile")
