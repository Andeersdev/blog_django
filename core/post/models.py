from django.db import models
from core.user.models import User


class Post(models.Model):

    title = models.CharField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to='post/', null=True, blank=True)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post'

    def __str__(self) -> str:
        return self.title


class Reactions(models.Model):

    likes = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reactions'


class Comments(models.Model):

    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'

    def __str__(self) -> str:
        return self.comment
