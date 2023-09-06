from django import forms
from .models import Property, Review, Thread, Comment, Message

class PropertyForm(forms.ModelForm):
    class Meta:
        model  = Property
        fields = "__all__"

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review_text"]

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "content"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
        labels = {
            "content": "Message"
        }