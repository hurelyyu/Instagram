import re

from django import template
from django.urls import NoReverseMatch, reverse
from Insta.models import Like


register = template.Library()

@register.simple_tag
def is_following(current_user, background_user):
    return background_user.get_followers().filter(creator=current_user).exists()

@register.simple_tag
def has_user_liked_post(post, user):
    try:
        #Like: 大熊猫， objects：胖胖，花花，萌兰
        #在所有的点赞中，找到跟传入参数一致的like，如果有就是full heart else空爱心
        like = Like.objects.get(post=post, user=user)
        return "fa-heart"
    except:
        return "fa-heart-o"

@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''