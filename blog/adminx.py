import requests
import xadmin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth import get_permission_codename
from django.contrib.admin.models import LogEntry

from xadmin.filters import RelatedFieldListFilter
from xadmin.filters import manager
from xadmin.layout import Row, Fieldset, Container

from .models import Post, Tag, Category
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
# Register your models here.

#权限管理API
PERMISSION_API =  "http://permission.sso.com/has_perm?user={}&perm_code={}"

class PostInline:
    form_layout = (
        Container(
            Row("title", "desc"),
        )
    )
    extra = 1 # 控制额外多几个
    model = Post


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "is_nav", "create_time", "psot_count")
    fields = ("name", "status", "is_nav")

    # inlines = [PostInline, ]
    def psot_count(self, obj):
        return obj.post_set.count()

    psot_count.short_description = "文章数量"


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "create_time")
    fields = ("name", "status")


class CategoryOwnerFilter(RelatedFieldListFilter):
    """
    自定义过滤器，只展示当前用户的的分类
    """
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ['title', 'category', 'status', 'create_time', 'owner', 'operator']
    list_display_links = []

    list_filter = ['category', ]
    search_fields = ['title', 'category__name']
    save_on_top = True

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True
    # 自动赋值当前用户
    exclude = ['owner']
    # 用fieldsets 替换 fields  自定义控制布局
    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
        )
    )

    # 自定义方法
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = "操作"

    # # 引入css和js
    # @property
    # def Media(self):
    #     # xadmin基于bootstrap，引入会页面样式冲突，仅供参考, 故注释。
    #     media = super().get_media()
    #     media.add_js(['https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js'])
    #     media.add_css({
    #             'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     })
    #     return media

