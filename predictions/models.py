from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.


class Event(models.Model):
    """
    This model represents a football event or match.
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    date = models.DateTimeField()
    featured_image = CloudinaryField('image', default='placeholder')
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="created_events")
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)
    result = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.title}"
    
class Comment(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=80, blank=True)
    email = models.EmailField(max_length=80, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)


    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
    

class Prediction(models.Model):
    PREDICTION_CHOICES = (
        ('X1', 'Team 1 Wins'),
        ('DRAW', 'Draw'),
        ('X2', 'Team 2 Wins'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="predictions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=10, choices=PREDICTION_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} predicted {self.get_prediction_display()} for {self.event.title}"
    
