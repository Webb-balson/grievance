from django import forms
from .models import Topic, Complain

class NewComplainForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Enter your complain here...'}
        ), 
        max_length=4000,
        help_text='The Textarea should have following fields to validate your complain: 1.Name 2. USN/StaffID 3. Other'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']

class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['message', ]