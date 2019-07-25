from django import forms
from .models import Topic, Complain

class NewComplainForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Your complaint should have (Full Name), (USN-Student), (ID-Faculty), (Ward_USN-Parent), (StaffID-Staff)'}
        ), 
        max_length=4000,
        help_text='Note: Without proper details, your complaint will be invalidated.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']

class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ['message', ]