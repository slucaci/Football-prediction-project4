from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.


class Event(models.Model):
    """
    This model represents a football event or match.
    """
    event_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="created_events")
    created_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)