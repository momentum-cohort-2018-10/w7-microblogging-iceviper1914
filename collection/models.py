from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    users_followed = models.ManyToManyField(to="user", through="Follow", through_fields=("following_user", "followed_user"), related_name="followers")


class Post(models.Model):
    title = models.CharField(max_length=255)
    voted_users = models.ManyToManyField(to=User, through='Vote', related_name='user_votes')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="vote")
    post = models.ForeignKey(to=Post, on_delete=models.SET_NULL, null=True, related_name="votes")

    class Meta:
        unique_together = (
            'user', 'post'
        )

    
class Follow(models.Model):
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follows_from")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name="follows_to")
    created_at = models.DateTimeField(auto_now_add=True, null=False)