from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False,blank=True,null=True)
    created_by = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Profile(models.Model):
    name = models.CharField(max_length=300,default="nun")
    # picture = models.ImageField(max_length=300,null=True,blank = True,upload_to='pictures/%Y/%m/%d/')
    picture = models.ImageField(max_length=300,default='default.png',null=True,blank = True,upload_to='pictures/')