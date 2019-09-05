import xadmin

from .models import Link, SiderBar
from typeidea.base_admin import BaseOwnerAdmin
# Register your models here.


@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ("title", "href", "status", "weight", "create_time")
    fields = ("title", "href", "status", "weight")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@xadmin.sites.register(SiderBar)
class SiderBarAdmin(BaseOwnerAdmin):
    list_display = ("title", "display_type", "content", "create_time")
    fields = ("title", "display_type", "content")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SiderBarAdmin, self).save_model(request, obj, form, change)
