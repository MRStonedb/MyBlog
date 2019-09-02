#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.contrib.admin import AdminSite


# 实现多后台
class CustomSite(AdminSite):
    site_header = "Typeidea"
    site_title = 'MyBlog 管理后台'
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')
