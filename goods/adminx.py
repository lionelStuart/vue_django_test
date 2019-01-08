import xadmin

from .models import GoodCategory, Goods, GoodCategoryBrand, Banner, GoodImage, IndexAd, HotSearchWords


class GoodsAdmin(object):
    list_display = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                    "shop_price", "goods_brief", "goods_desc", "is_new", "is_hot", "add_time"]
    search_fields = ['name', ]
    list_editable = ["is_hot", ]
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                   "shop_price", "is_new", "is_hot", "add_time", "category__name"]
    style_fields = {"goods_desc": "ueditor"}

    # inline??

    class GoodsImagesInline(object):
        model = GoodImage
        exclude = ["add_time"]
        extra = 1
        style = 'tab'

    """
    内联类
    """
    inlines = [GoodsImagesInline]


class GoodCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


class GoodBrandAdmin(object):
    list_display = ["category", "image", "name", "desc"]

    """
    do what?
    """

    def get_context(self):
        context = super(GoodBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodCategory.objects.filter(category_type=1)
        return context


class BannerAdmin(object):
    list_display = ["goods", "image", "index"]


class IndexAdAdmin(object):
    list_display = ["category", "goods"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(GoodCategoryBrand, GoodBrandAdmin)
xadmin.site.register(GoodCategory, GoodCategoryAdmin)
xadmin.site.register(Goods, GoodsAdmin)

xadmin.site.register(IndexAd, IndexAdAdmin)
xadmin.site.register(HotSearchWords, HotSearchAdmin)

