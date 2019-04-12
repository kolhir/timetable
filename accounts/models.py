from django.db import models
from timetable.models import Group
from django.contrib.auth.models import User
# Create your models here.

class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tt_json = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null = True)
    