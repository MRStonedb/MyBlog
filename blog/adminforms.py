#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django import forms

# 让文章描述能够多行多列显示
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label="摘要", required=False)