from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

def post_pic(instance,filename):
	return 'postpics/{0}/{1}'.format(instance.id,filename)
CHOICES = (
	('comming' ,'comming soon'),
        ('learn', 'learing'),
        ('electrical', 'Electrical'),
        ('fashion',"Fashion"),
        ('games', 'Games'),
        ('house', 'House'),
        ('office', 'office'),
        ('outdoor', 'outdoor'),
        ('other', 'other')
)
class Post(models.Model):
	title = models.CharField(max_length = 255)
	disc = models.TextField(null=True,blank =True)
	date_posted = models.DateTimeField(auto_now_add=True)
	user_name = models.ForeignKey(User,on_delete=models.CASCADE)
	price = models.IntegerField(null= True,blank=True)
	buyurl = models.URLField(max_length=255,blank=True,null=True)
	tags = models.CharField(max_length=100,choices = CHOICES,default = '1')
	adminchoose = models.CharField(max_length = 300,null=True,blank=True)

	def __str__(self):
		return self.title
class PostImages(models.Model):
	Imgtitle = models.ForeignKey(Post,related_name='img',on_delete=models.CASCADE)
	pimages = models.FileField(upload_to='post_pic',null=True,blank=True)

class comments(models.Model):
	post = models.ForeignKey(Post,related_name='details',on_delete=models.CASCADE)
	username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
	comment = models.CharField(max_length=2000,blank=True)
	comment_date = models.DateTimeField(auto_now_add=True)
	reply = models.ForeignKey('comments', on_delete=models.CASCADE, related_name="replies", null=True)

class Like(models.Model):
	user = models.ForeignKey(User,related_name='likes', on_delete=models.CASCADE)
	post = models.ForeignKey(Post,related_name='likes', on_delete=models.CASCADE)
class Rating(models.Model):
	user = models.ForeignKey(User,related_name='rates', on_delete=models.CASCADE)
	post = models.ForeignKey(Post,related_name='rates', on_delete=models.CASCADE)
	rating = models.IntegerField(default=0,
		validators =[
		MaxValueValidator(5),
		MinValueValidator(0)
		])




