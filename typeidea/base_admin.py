#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    """
    1. 用来自动补充文章，分类，标签，侧边栏，友链这些model的owner字段
    2. 用来针对queyset 过滤当前用户
    """
    #只显示当前用户自己创建的文章
    def get_queryset(self, request):
        queryset = super(BaseAdmin, self).get_queryset(request)
        return queryset.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseAdmin, self).save_model(request, obj, form, change)
