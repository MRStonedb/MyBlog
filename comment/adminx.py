#from django.contrib import admin
import xadmin

from .models import Comment


@xadmin.sites.register(Comment)
class CommentAdmin:
    list_display = ("target", "nickname", "content", "website", "create_time")
