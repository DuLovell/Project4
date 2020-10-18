from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
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

class Follow(models.Model):
	user_to_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_followers")
	followers = models.ManyToManyField(User, blank=True, related_name="follows")

	def __str__(self):
		user_str = ""
		for user in self.followers.all():
			user_str += user.username + ", "
		user_str = user_str.rstrip(", ")
		return f"{user_str} following {self.user_to_follow}"