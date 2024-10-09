from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from .models import Event
from .forms import CommentForm
from .models import Event, Prediction
from .forms import PredictionForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def user_predictions(request):
    predictions = Prediction.objects.filter(user=request.user)

    return render(request, 'predictions/user_predictions.html', {'predictions': predictions})


class EventList(generic.ListView):
    queryset = Event.objects.filter(status=1)
    template_name = "predictions/index.html"
    paginate_by = 6


def event_detail(request, slug):

    queryset = Event.objects.filter(status=1)
    event = get_object_or_404(queryset, slug=slug)

    comments = event.comments.all().order_by("-created_on")
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
