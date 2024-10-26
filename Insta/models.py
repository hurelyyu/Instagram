from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from imagekit.models import ProcessedImageField


# Create your models here.
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles',
        format='JPEG',
        options={'quality': 100},
        null=True,
        blank=True,
        )
    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])
    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

    # def get_absolute_url(self):
    #     return reverse('profile', args=[str(self.id)])

    # def __str__(self):
    #     return self.username

class Post(models.Model):
    author = models.ForeignKey( # a foreign key indicate a Many-To-One relationship
        InstaUser, #foreign key is InstaUser
        blank=True,
        null=True,
        on_delete=models.CASCADE, # delete this author will delete all his posts
        related_name='my_posts', # we can use author.posts to get all posts belong to this user
        )
    title = models.TextField(blank = True, null = True)
    image = ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        )
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    def get_like_count(self):
        return self.likes.count()
        

class Like(models.Model):
    #Like model define the relation of other models, use ForeignKey  
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, 
        related_name='likes',
        )
    user = models.ForeignKey(
        InstaUser, on_delete=models.CASCADE
        )

    class Meta:
        unique_together = ("post", "user")

    # define how the relation likes show in admin
    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set") #got all A follow 的 user
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set") #.friend_set: get all users following A

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username
