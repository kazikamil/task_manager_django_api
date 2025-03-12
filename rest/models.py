from django.db import models
from django.contrib.auth.models import User

class Project (models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200,null=False)
    date_start=models.DateField()
    date_end=models.DateField()


class Task (models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=50,null=False,blank=False)
    description=models.CharField(max_length=500)
    duration=models.DurationField()

# Create your models here.
