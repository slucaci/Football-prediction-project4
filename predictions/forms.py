from django import forms
from .models import Comment
from .models import Prediction

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['prediction']
        widgets = {
            'prediction': forms.RadioSelect
        }