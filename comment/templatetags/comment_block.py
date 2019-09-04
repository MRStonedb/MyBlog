from django import template

from comment.forms import CommentForm
from comment.models import Comment

"""
用于抽象出评论组件，让评论模块即插即用，比如在友链页和详情页均可展示评论
"""
register = template.Library()

@register.inclusion_tag('comment/block.html')
def comment_block(target):
    return{
        'target': target,
        'comment_form': CommentForm(),
        'comment_list': Comment.get_by_target(target),
    }
