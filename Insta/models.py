from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractUser

# Create your models here.
# 
class InstaUser(AbstractUser):
	profile_pic = ProcessedImageField(
		upload_to = 'static/images/profile_pic',
		format = 'JPEG',
		options = {'quality' : 100},
		blank = True,
		null = True
		)

class Post(models.Model):
	author = models.ForeignKey(
		InstaUser,
		on_delete = models.CASCADE,
		related_name = 'my_posts'
	)
	title = models.TextField(blank = True, null = True)
	image = ProcessedImageField(
		upload_to = 'static/images/posts',
		format = 'JPEG',
		options = {'quality' : 100},
		blank = True,
		null = True
		)
	def get_like_count(self):
		return self.likes.count() # .likes 获得related name
	def get_absolute_url(self):
		return reverse("posts_detail", args = [str(self.id)])

# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)
#     user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=100)
#     posted_on = models.DateTimeField(auto_now_add=True, editable=False)

#     def __str__(self):
#         return self.comment

class Like(models.Model):
	post = models.ForeignKey(
		Post,
		on_delete = models.CASCADE, #删除post时，删除所有like
		related_name = 'likes' #当出于此post object，获得所有like此object的object
	) #指向外面的Post
	user = models.ForeignKey(
		InstaUser,
		on_delete = models.CASCADE,
		related_name = 'likes' #找到点过的所有的like
	) #指向InstaUser model

	class Meta:
		unique_together = ("post", "user") #同样的user和post只存在一次

	def __str__(self): #用一个string表示like
		return 'Like: ' + self.user.username + 'likes' + self.post.title