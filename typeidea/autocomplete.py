from dal import autocomplete

from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:  # 判断用户是否登陆
            return Category.objects.none()  # 未登录的用户直接返回空的queryset 

        qs = Category.objects.all()  # 获取该用户创建的所有分类

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):  # get_queryset 输入的是： self.q,是请求参数传递过来的值  返回： queryset
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all() # 获取该用户创建的所有标签

        if self.q:  # 判断是否存在self.q  
            qs = qs.filter(name__istartswith=self.q)
        return qs
