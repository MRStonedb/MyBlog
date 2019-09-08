#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from rest_framework import serializers, pagination

from .models import Post, Category

"""
list/detail 返回的字段都相同，字段无限制
"""
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['title', 'category', 'desc', 'content_html', 'create_time']

"""
为不同的api接口定义不同的返回字段,并对相应的字段做限制
"""
class PostSerializer(serializers.HyperlinkedModelSerializer):
    # HyperlinkedModelSerializer  使得操作api像操作网页一样，可以点击
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    url = serializers.HyperlinkedIdentityField(view_name='api-post-detail')

    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'category', 'tag', 'owner', 'create_time']



class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'content_html', 'create_time']



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'create_time']



class CategoryDetailSerializer(CategorySerializer):
    posts = serializers.SerializerMethodField('paginated_posts')
    def paginated_posts(self,obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request':self.context['request']})
        return {
            'count':posts.count(),
            'results':serializer.data,
            'previous':paginator.get_previous_link(),
            'next':paginator.get_next_link(),
            }

    class Meta:
        model = Category
        fields = ['id', 'name', 'create_time', 'posts']
    
