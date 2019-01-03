import xadmin

from goods.models import GoodCategory, Goods


class GoodsAdmin(object):
    list_display = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                    "shop_price", "goods_brief", "is_new", "is_hot", "add_time"]  #, "goods_desc"
    search_fields = ['name', ]
    list_editable = ["is_hot", ]
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                   "shop_price", "is_new", "is_hot", "add_time", "category__name"]
    style_fields = {"goods_desc": "ueditor"}

    # inline??
    # inlines = [GoodsImagesInline]


class GoodCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


class GoodCategoryBrandAdmin(object):
    pass


xadmin.site.register(GoodCategory, GoodCategoryAdmin)
xadmin.site.register(Goods, GoodsAdmin)
