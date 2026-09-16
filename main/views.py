from django.shortcuts import render
from main.forms import ExperienceForm
from main.models import Experience, Education
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render



def show_main(request):
    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "hero_name1": "Rebecca Love",
        "hero_name2": "Lianov Simanjuntak",
        "npm": "2506637110",
        "study_program": "S1 Ilmu Komputer KKI",
        "bio": (
            "A deeply driven undergraduate student striving to create tech solutions for a better life. As an enthusiast in AI/ML, I'm eager to learn how this field can address complex issues ranging from cybersecurity to biomedical sciences, as I continue to collaborate, learn, and grow as a problem-solver."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience succesfully added!")
        return redirect("main:show_experience")

    context = {
        "name": "Rebecca",
        "form": form,
    }
    return render(request, "experience_form.html", context)