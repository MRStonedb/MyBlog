from django.contrib import admin

from .models import Link, SiderBar
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseAdmin
# Register your models here.


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseAdmin):
    list_display = ("title", "href", "status", "weight", "create_time")
    fields = ("title", "href", "status", "weight")



@admin.register(SiderBar, site=custom_site)
class SiderBarAdmin(BaseAdmin):
    list_display = ("title", "display_type", "content", "create_time")
    fields = ("title", "display_type", "content")
