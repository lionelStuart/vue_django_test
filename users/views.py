import traceback
from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
# oh no
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from users.models import VerifyCode
from users.serializers import UserRegSerializer, UserDetailSerializer, SmsSerializer
from utils.yunpian import YunPian
from vue_django_test.settings import APIKEY

User = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("use custom backend")
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print("CustomBack e:{}".format(e))
            traceback.print_exc()
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        Gen 4-rnd-code
        :return:
        """
        seeds = "0123456789"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        """
        创建smsCode 时 使用 yunpian
        1.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        print("on create new sms code resp ")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        yun_pian = YunPian(APIKEY)

        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status['code'] != 0:
            print("bad request")
            return Response(
                {'mobile': sms_status['msg']},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({'mobile': mobile},
                            status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    """
    use djangorestframework-jwt
    1.pip install djangorestframe-jwt
    2.setting 配置DEFAULT auth
    3.配置url 到 rest_framework.urls
    4.url：
    /login
    /code ->/users
    5.添加中间件-验证环节 CustomBackend(ModelBackend):
    setting: AUTHENTICATION_BACKENDS
    6.添加短信发送服务 需要注册api 服务 写入key 匹配的topic
    
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            print("return action retrive")
            return UserDetailSerializer
        elif self.action == "create":
            print("return action create")
            return UserRegSerializer

        return UserDetailSerializer

    # permission_classes = (permissions.IsAuthenticated, )
    def get_permissions(self):
        if self.action == "retrieve":
            print("get_permission retrive")
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            print("get no permisson")
            return []

        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
