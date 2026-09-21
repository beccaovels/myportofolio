from django import forms
from django.forms.models import ModelForm
from main.models import Experience, Skill


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


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            'name',
            'description',
            'logo_url',
            'years_of_experience',
        ]

        labels = {
            'name': 'Technology Name',
            'description': 'Description',
            'logo_url': 'Logo URL',
            'years_of_experience': 'Years of Experience',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Python, React',
                    'maxlength': 255,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'A brief description',
                    'rows': 3,
                }
            ),
            'logo_url': forms.URLInput(
                attrs={
                    'placeholder': 'https://...',
                }
            ),
            'years_of_experience': forms.NumberInput(
                attrs={
                    'placeholder': 'e.g. 3',
                    'min': 0,
                }
            ),
        }