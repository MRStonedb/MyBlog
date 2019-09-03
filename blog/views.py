import traceback
from django.db.models import Q
from django.shortcuts import render, get_object_or_404


from .models import Post, Tag, Category
from config.models import SiderBar
from comment.forms import CommentForm
from comment.models import Comment
from django.views.generic import DetailView, ListView

# Create your views here.


# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None

#     context = {
#         'post':post,
#         'sidebars':SiderBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)


# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None

#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()

#     context = {
#         'category':category,
#         'tag':tag,
#         'post_list': post_list,
#         'sidebars':SiderBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)


class CommonViewMixin:
    # def get_content_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # try:
        #     ss = SiderBar.get_all()
        #     print("===========", ss)
        # except Exception as e:
        #     print(traceback.format_exc())
        
        # context.update({
        #     'sidebars':SiderBar.get_all(),
        # })
        # context.update(Category.get_navs())
        # return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': self.get_sidebars(),
        })
        context.update(self.get_navs())
        return context

    def get_sidebars(self):
        return SiderBar.objects.filter(status=SiderBar.STATUS_SHOW)

    def get_navs(self):
        categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories,
        }

class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_content_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category':category,
        })
        return context

    def get_queryset(self):
        """
        重写get_queryset，根据分类过滤
        """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_content_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Category, pk=tag_id)
        context.update({
            'tag':tag,
        })
        return context

    def get_queryset(self):
        """
        重写get_queryset，根据标签过滤
        """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)
    

class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    pk_url_kwarg = "post_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form':CommentForm,
            'comment_list':Comment.get_by_target(self.request.path),
        })
        return context


class SearchView(IndexView):
    def get_content_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'keyword':self.request.GET.get("keyword", "")
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("keyword")
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.request.GET.get("owner_id")
        return queryset.filter(owner_id=author_id)
        
