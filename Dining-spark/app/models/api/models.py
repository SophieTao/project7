from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
	username = models.CharField(max_length=100, unique=True)
	email = models.CharField(max_length=100, unique=True, null=True)
	password = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.username

class Authenticator(models.Model):
	user_id = models.PositiveIntegerField(null=True)
	authenticator = models.CharField(primary_key=True, max_length=255)
	date_created = models.DateTimeField()

	def __str__(self):
		return self.user_id
	

# Create your models here.
class Cafe(models.Model):
	name = models.CharField(max_length=100,null=True)
	location = models.CharField(max_length=50,null=True)
	date = models.DateTimeField(null=True)
	description = models.CharField(max_length = 1000,null=True)
	Calories = models.PositiveIntegerField(null = True)

	def __str__(self):
		return self.name

class Comment(models.Model):
	description = models.CharField(max_length=1300)
	feedback = models.CharField(max_length=300)
	date_written = models.DateTimeField(null=True) 
	rating = models.PositiveIntegerField(null=True,validators=[MinValueValidator(1), MaxValueValidator(5),])

	def __str__(self):
		return self.description

	def get_absolute_url(self):
		return reverse('comment-update', kwargs={'pk': self.pk})

class Recommendation(models.Model):
	item_id = models.PositiveIntegerField()
	recommended_items = models.TextField()