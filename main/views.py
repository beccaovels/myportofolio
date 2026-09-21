from django.shortcuts import render
from main.forms import ExperienceForm, SkillForm
from main.models import Experience, Education, Skill
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
        "name": "Rebecca Love Lianov Simanjuntak",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Experience.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def show_experience(request):
    json_response = get_experience_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Rebecca Love Lianov SImanjuntak",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def delete_experience(request, project_id):
    project = get_object_or_404(Experience, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Experience deleted successfully!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def get_skills_json(request):
    """
    Retrieve all Skill objects from the database and serialize them into JSON format.
    Supports optional case-insensitive filtering by the 'name' query parameter.
    """
    title_query = request.GET.get("name", "").strip()
    skills = Skill.objects.all()

    if title_query:
        skills = skills.filter(name__icontains=title_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")


def show_skills(request):
    """
    Render the main skills page by first fetching the JSON data via get_skills_json,
    deserializing it back into Django model instances, and passing it to the template.
    """
    json_response = get_skills_json(request)

    skills_deserialized = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [s.object for s in skills_deserialized]
    title_query = request.GET.get("name", "").strip()

    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "skill_list": skills,
        "title_query": title_query,
    }
    return render(request, "skills.html", context)


def create_skill(request):
    """
    Handle the creation of a new Skill object using a ModelForm.
    If the request is POST and valid, saves the skill and redirects.
    """
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New skill successfully added!")
        return redirect("main:show_skills")

    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "form": form,
    }
    return render(request, "skill_form.html", context)


def update_skill(request, id):
    """
    Handle the modification of an existing Skill object using a ModelForm.
    If the request is POST and valid, updates the skill and redirects.
    """
    skill = get_object_or_404(Skill, pk=id)
    form = SkillForm(request.POST or None, instance=skill)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill updated successfully!")
        return redirect("main:show_skills")

    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "form": form,
        "is_update": True,
    }
    return render(request, "skill_form.html", context)


def delete_skill(request, id):
    """
    Handle the deletion of an existing Skill object.
    Only allows deletion via POST requests for security.
    """
    skill = get_object_or_404(Skill, pk=id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill deleted successfully!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")