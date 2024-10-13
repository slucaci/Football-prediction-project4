from django.test import TestCase
from .forms import CommentForm, PredictionForm
from .models import Comment, Prediction
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Event

class CommentFormTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="AC Milan vs AS Roma",
            slug="ac-milan-vs-as-roma",
            status=1,
            date=timezone.now()
        )
    
    def test_comment_form_valid(self):
        """Test if the CommentForm is valid with proper data"""
        form_data = {
            'name': 'Test User',
            'email': 'testuser@test.com',
            'body': 'Test Comment'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_comment_form_invalid(self):
        """Test if the CommentForm is invalid when required fields are missing"""
        form_data = {
            'name': '',
            'email': 'testuser@test.com',
            'body': 'Test comment'
        }
        form = CommentForm(data=form_data)
        print(form.errors)
        self.assertFalse(form.is_valid())

class PredictionFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword12345')
        self.event = Event.objects.create(
            title="AC Milan vs AS Roma",
            slug="ac-milan-vs-as-roma",
            status=1,
            date=timezone.now()
        )

    def test_prediction_form_valid(self):
        """Test if the PredictionForm is valid with proper data"""
        form_data = {
            'prediction': 'X1'
        }
        form = PredictionForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_prediction_form_invalid(self):
        """Test if the PredictionForm is invalid when no data is provided"""
        form_data = {
            'prediction': ''
        }
        form = PredictionForm(data=form_data)
        self.assertFalse(form.is_valid())
