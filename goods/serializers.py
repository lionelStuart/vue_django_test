from rest_framework import serializers

from .models import GoodCategory, GoodCategoryBrand, GoodImage, Goods


class CategorySerializer3(serializers.ModelSerializer):
    """
    三级目录
    """

    class Meta:
        model = GoodCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    二级目录
    """
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodCategory
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodCategoryBrand
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"
