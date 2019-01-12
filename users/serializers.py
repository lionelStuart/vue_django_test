from datetime import timedelta

from django.utils import timezone as datetime

import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import VerifyCode
from vue_django_test.settings import REGEX_MOBILE

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        can not alloweed two user on one ie
        :param data:
        :return:
        """
        print("do validate mobile")
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")
        #
        # # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")
        #
        # # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def validated_code(self, code):
        ## 同用户的验证取最后一条
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']) \
            .order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            ## 验证条件 超时 错误
            five_min_ago = datetime.now() - datetime.timedelta(hours=0, minutes=0, seconds=0)
            if five_min_ago > last_record.add_time:
                raise serializers.ValidationError("验证码超时")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        print("on validate ")
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')
