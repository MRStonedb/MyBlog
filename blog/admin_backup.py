import requests
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth import get_permission_codename
from django.contrib.admin.models import LogEntry

from .models import Post, Tag, Category
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseAdmin
# Register your models here.

#权限管理API
PERMISSION_API =  "http://permission.sso.com/has_perm?user={}&perm_code={}"

class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1 # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseAdmin):
    list_display = ("name", "status", "is_nav", "create_time", "psot_count")
    # fields = ("name", "status", "is_nav", "owner")
    fields = ("name", "status", "is_nav")

    inlines = [PostInline, ]

    def psot_count(self, obj):
        return obj.post_set.count()

    psot_count.short_description = "文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseAdmin):
    list_display = ("name", "status", "create_time")
    fields = ("name", "status")


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    自定义过滤器，只展示当前用户的的分类
    """
    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseAdmin):

    list_display = ("title", "category", "status", "create_time", "owner", "operator")
    list_display_links = ()
    # list_filter = ["category", CategoryOwnerFilter]
    list_filter = [CategoryOwnerFilter]
    search_fields = ["title", "category__name"]
    actions_on_top = True
    actions_on_bottom = True

    # 自动赋值当前用户
    exclude = ('owner', )

    # 让文章描述能够多行多列显示
    form = PostAdminForm

    #编辑页面
    save_on_top = True

    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    # 用fieldsets 替换 fields  自定义控制布局
    fieldsets = (
        ('基础配置', {
            'fields':(
                ('category', 'title'),
                'status',
            ),
        }),
        ('内容', {
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('其他', {
            # 'classes':('collapse',), # 给配置的板块加上css属性
            'fields':(
                'tag',
            ),
        })
    )


    # 自定义方法
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = "操作"

    """
    # 操作权限
    def has_add_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('add', opts)
        perm_code = "%s.%s" %(opts.app_label, codename)
        resp = requests.get(PERMISSION_API.format(request.user.username, perm_code))
        if resp.status_code == 200:
            return True
        else:
            return False
    """

    # 引入css和js
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


# admin 查看日志
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["object_repr", "object_id", "action_flag", "user", "change_message"]
