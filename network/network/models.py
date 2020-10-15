from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.CharField(max_length=32)
	text = models.TextField(max_length=280)
	liked = models.ManyToManyField(User, blank=True, related_name="post_liked")
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user}: {self.text}"

class Like(models.Model):
	user = models.CharField(max_length=32)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

	def __str__(self):
		return f"{self.user} liked {self.post}"