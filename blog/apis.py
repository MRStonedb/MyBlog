#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# from rest_framework import generics
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Post,Category
from .serializers import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer


# @api_view()
# def Post_list(request):
#     posts = Post.objects.filter(status=Post.STATUS_NORMAL)
#     post_serializers = PostSerializer(posts, many=True)
#     return Response(post_serializers.data)

# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
#     serializer_class = PostSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    permission_classes = [IsAdminUser]

    def retrieve(self,request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    # 获取某个分类下的文章的方法
    # def filter_queryset(self, queryset):
    #     category_id = self.request.query_params.get('category')
    #     if category_id:
    #         queryset = queryset.filter(category_id=category_id)
    #     return queryset


class CategoryViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    #实现 可以获取某个分类下的文章的方法 功能
    def retrieve(self,request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)
