from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    creation_time = models.DateTimeField()

    def __str__(self):
        return f"id:{self.id}, text:{self.text}"

class Comment(models.Model):
    text = models.CharField(max_length=200)
    creation_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"id:{self.id}, text:{self.text}"

class Profile(models.Model):
    picture = models.FileField(blank=True)
    content_type = models.CharField(blank=True, max_length=50)
    bio = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    following = models.ManyToManyField(User, related_name="followers")

    def __str__(self):
        return f"id:{self.id}, text:{self.user.first_name}"