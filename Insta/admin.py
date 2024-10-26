from django.contrib import admin

# Register your models here.
# from Insta.models import Comment, InstaUser, Like, Post, UserConnection
from Insta.models import Post, InstaUser,Like,UserConnection
# admin.site.register(Post, PostAdmin)
admin.site.register(Post)
admin.site.register(InstaUser)
admin.site.register(Like)
admin.site.register(UserConnection)