from django.db import models

# Create your models here.
class About(models.Model):
    """
    This model represents the about page.
    """
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title