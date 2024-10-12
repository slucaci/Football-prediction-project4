from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib import messages
from .models import Event
from .forms import CommentForm
from django.db.models import Count, F, Case, When, IntegerField
from .models import Event, Prediction, Comment
from .forms import PredictionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import timezone


# Create your views here.


@login_required
def user_predictions(request):
    """This view displays a list of predictions made by the current user."""
    predictions = Prediction.objects.filter(user=request.user)

    return render(request, 'predictions/user_predictions.html', {'predictions': predictions})


class EventList(generic.ListView):
    """This view displays a list of events."""
    queryset = Event.objects.filter(status=1) # This line of code will filter events that have a status of 1(Published) 
    queryset.filter(date__lt=timezone.now()).update(status=0) # This line of code will update the status of events that have already occurred to 0(https://stackoverflow.com/questions/24211293/django-queryset-filter-gt-lt-gte-lte-returns-full-object-list) used stackoverflow to help me with this line of code
    template_name = "predictions/index.html"
    paginate_by = 6


def event_detail(request, slug):
    """This view displays the details of a single event."""

    queryset = Event.objects.filter(status=1) # This line of code will filter events that have a status of 1(Published)
    event = get_object_or_404(queryset, slug=slug) 

    comments = event.comments.all().order_by("-created_on") # This line of code will order the comments by the created_on field in descending order
    comment_count = event.comments.filter(active=True).count()

    if request.method == "POST" and 'submit_comment' in request.POST:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.event = event
            comment.save()
            messages.success(request, 'Comment submitted and awaiting approval')
            return redirect('event_detail', slug=event.slug)
    else:
        comment_form = CommentForm()

    try:
        existing_prediction = Prediction.objects.get(event=event, user=request.user) 
        prediction_form = PredictionForm(instance=existing_prediction)
    except Prediction.DoesNotExist:
        existing_prediction = None
        prediction_form = PredictionForm()

    if request.method == 'POST' and 'submit_prediction' in request.POST:
        if existing_prediction:
            prediction_form = PredictionForm(request.POST, instance=existing_prediction) 
        else:
            prediction_form = PredictionForm(request.POST)

        if prediction_form.is_valid():
            prediction = prediction_form.save(commit=False) 
            prediction.user = request.user
            prediction.event = event
            prediction.save()
            messages.success(request, 'Your prediction has been saved.')
            return redirect('event_detail', slug=event.slug)

    return render(
        request,
        "predictions/event_detail.html",
        {
            "event": event,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
            "prediction_form": prediction_form,
            "existing_prediction": existing_prediction,
        },
    )

def leaderboard(request):
    """This view displays a leaderboard of users based on the number of correct predictions."""
    users = User.objects.exclude(username='admin') # This line of code will exclude the admin user from the leaderboard
    leaderboard_data = [] 
    for user in users:
        total_predictions = Prediction.objects.filter(user=user).count() # This line of code will count the total number of predictions made by a user
        correct_predictions = Prediction.objects.filter(
            user=user,
            prediction=F('event__result')
        ).count() # This line of code will count the number of correct predictions made by a user
        leaderboard_data.append({
            'username': user.username,
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions,
        }) # This line of code will append the user's username, total predictions and correct predictions to the leaderboard_data list
    leaderboard_data = sorted(leaderboard_data, key=lambda x: x['correct_predictions'], reverse=True)
    return render(request, 'predictions/leaderboard.html', {'leaderboard_data': leaderboard_data})

def edit_comment(request, slug, comment_id):
    """
    Allow users to edit their own comments.
    """
    comment = get_object_or_404(Comment, id=comment_id) 
    
    # Only handle POST requests
    if request.method == "POST":
        
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid() and comment.author == request.user:
            comment.active = False  # Set comment inactive after edit, waiting for approval
            comment.save()
            messages.success(request, "Comment updated and awaiting approval!")
        else:
            messages.error(request, "Error updating comment.")
        return HttpResponseRedirect(reverse('event_detail', args=[slug]))

    # If the request method is not POST, redirect back to the event detail page
    return HttpResponseRedirect(reverse('event_detail', args=[slug]))


def delete_comment(request, slug, comment_id):
    """This view allows users to delete their own comments."""
    comment = get_object_or_404(Comment, id=comment_id, event__slug=slug)

    if comment.author != request.user:
        messages.error(request, "You can only delete your own comments.")
        return HttpResponseRedirect(reverse('event_detail', args=[slug]))

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
    else:
        messages.error(request, "Invalid request method.")
    
    return HttpResponseRedirect(reverse('event_detail', args=[slug]))