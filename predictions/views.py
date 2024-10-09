from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Event
from .forms import CommentForm

# Create your views here.

class EventList(generic.ListView):
    queryset = Event.objects.filter(status=1)
    template_name = "predictions/index.html"
    paginate_by = 6

def event_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Event.objects.filter(status=1)
    event = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "predictions/event_detail.html",
        {"event": event},
    )