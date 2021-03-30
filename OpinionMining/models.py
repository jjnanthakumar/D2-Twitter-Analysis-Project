from django.db import models
from tweepy.models import Model
from django.contrib.auth.models import User
# Create your models here.

class Twitter(models.Model):
    # store images in clodinary storage or as a string
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    json_data = models.TextField(null=False,default="{}")