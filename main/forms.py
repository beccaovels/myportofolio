import re
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
            'logo_url',
            'description',
        ]

        labels = {
            'name': 'Technology Name',
            'logo_url': 'Logo URL',
            'description': 'Description',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Python, React',
                    'maxlength': 255,
                }
            ),
            'logo_url': forms.URLInput(
                attrs={
                    'placeholder': 'https://...',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'A brief description',
                    'rows': 3,
                }
            ),
        }

    def clean_logo_url(self):
        url = self.cleaned_data.get('logo_url')
        if url and 'drive.google.com/file/d/' in url:
            # Automatically convert Google Drive 'view' links to raw image 'thumbnail' links
            match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
            if match:
                file_id = match.group(1)
                return f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"
        return url