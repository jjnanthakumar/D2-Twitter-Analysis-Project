from django.db import models
from tweepy.models import Model

# Create your models here.

class Twitter(models.Model):
    hashtag= models.TextField(null=False, default="", max_length=200)
    # store images in clodinary storage