from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class List(models.Model):
    """Класс, который описывает список дел"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_opened = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """Класс, который описывает конкретное дело в списке"""
    list = models.ForeignKey(List, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
