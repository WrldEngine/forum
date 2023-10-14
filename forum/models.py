import hashlib
import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser

class ForumUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_photos', null=True)
    verified = models.BooleanField(null=True, default=False)
    unique_token = models.TextField(null=True)
    grade = models.IntegerField(null=True)
    email = models.EmailField(unique=True)
    post_creating = models.BooleanField(null=True, default=False)

    def generate_token(self):
        hash_code = secrets.token_hex(16)
        self.unique_token = hash_code

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"

class Questions(models.Model):
    image = models.ImageField(upload_to='questions', null=True)
    subject = models.TextField()
    title = models.CharField(max_length=10000, unique=True)
    content = models.TextField()
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Question"

class Answers(models.Model):
    image = models.ImageField(upload_to='answers', null=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    content = models.CharField(max_length=10000)
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Answer"

class Posts(models.Model):
    title = models.CharField(max_length=20000)
    content = models.TextField()
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Post"