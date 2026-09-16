from django import forms
from django.forms.models import ModelForm
from main.models import Experience


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            'title',
            'employer',
            'description',
            'category',
            'started_at',
            'ended_at',
        ]

        labels = {
            'title': 'Experience Title',
            'employer': 'Organisation / Company / Event Name',
            'description': 'Experience',
            'category': 'Category',
            'started_at': 'Start Date',
            'ended_at': 'End Date',
        }

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Experience title & role',
                    'maxlength': 255,
                }
            ),
            'employer': forms.TextInput(
                attrs={
                    'placeholder': 'Organisation / Company / Event you worked for',
                    'maxlength': 255,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Tell us about this experience',
                    'rows': 4,
                }
            ),
            'category': forms.RadioSelect(),
            'started_at': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'ended_at': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }