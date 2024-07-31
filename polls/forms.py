from django import forms
from .models import Poll, Choice, Category

class PollAddForm(forms.ModelForm):

    choice1 = forms.CharField(label='Choice 1', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice2 = forms.CharField(label='Choice 2', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll
        fields = ['text', 'category', 'choice1', 'choice2']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text', 'category']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
