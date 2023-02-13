from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
import datetime

class Blogpost(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Title=models.CharField(max_length=250)
    # Auth_name=models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE
    # )
    Blog_img=models.ImageField(upload_to='blog_image')
    Description=models.TextField()
    Blog_txt=models.TextField()
    Date=models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.Title
