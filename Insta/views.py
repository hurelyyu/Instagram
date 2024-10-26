#from django.shortcuts import render
from annoying.decorators import ajax_request
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from Insta.forms import CustomUserCreationForm
# from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import TemplateView, ListView, DetailView
# Create your views here.
# HelloWorld inherent TemplateView
# from Insta.models import InstaUser, Post, UserConnection, Like, Comment
from Insta.models import Post, Like, InstaUser, UserConnection

class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostsView(ListView):
    model = Post
    template_name = "index.html"
    # login_url = "login"
    # only show user post that we followed
    def get_queryset(self):
        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
            following.add(conn.following)
        return Post.objects.filter(author__in=following)

class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_datas(**kwargs)
    #     liked = Like.objects.filter(post=self.kwargs.get('pk'), user=self.request.user).first()
    #     if liked:
    #         data['liked'] = 1
    #     else:
    #         data['liked'] = 0
    #     return data
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    fields = '__all__'
    login_url = 'login'


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'
    
class UserUpdateView(UpdateView):
    model = InstaUser
    template_name = 'user_update.html'
    fields = ['profile_pic', 'username']

# import logging
# from django.http import JsonResponse
# from .models import Post
# logger = logging.getLogger(__name__)
@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    #get the post object which get the like request
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        #把上面创建的object保存到database
        like.save()
        result = 1
    #如果数据库已经存在post，request.user的pair了，则证明用户想要取消点赞
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }
    # logger.info(f"Request method: {request.method}")
    # if request.method == 'POST':
    #     post_pk = request.POST.get('post_pk')
    #     logger.info(f"Post PK: {post_pk}")
    #     if post_pk:
    #         try:
    #             post = Post.objects.get(pk=post_pk)
    #             logger.info(f"Post found: {post}")
    #             return JsonResponse({'result': True, 'post_pk': post_pk})
    #         except Post.DoesNotExist:
    #             logger.error(f"Post not found for pk: {post_pk}")
    #             return JsonResponse({'result': False, 'error': 'Post not found'})
    #     else:
    #         logger.error("No post_pk provided")
    #         return JsonResponse({'error': 'post_pk is missing'}, status=400)
    # logger.error("Invalid request method")
    # return JsonResponse({'error': 'Invalid request'}, status=400)