from django.shortcuts import render
from main.forms import ExperienceForm, SkillForm
from main.models import Experience, Education, Skill
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "hero_name1": "Rebecca Love",
        "hero_name2": "Lianov Simanjuntak",
        "npm": "2506637110",
        "study_program": "S1 Ilmu Komputer KKI",
        "bio": (
            "A deeply driven undergraduate student striving to create tech solutions for a better life. As an enthusiast in AI/ML, I'm eager to learn how this field can address complex issues ranging from cybersecurity to biomedical sciences, as I continue to collaborate, learn, and grow as a problem-solver."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response



def show_education(request):
    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Only the portfolio owner can add experiences."},
            status=403,
        )
    
    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience added successfully.", "pk": str(experience.id)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related('starred_by').all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    # Manually build the JSON data so we can add the Star logic
    data = []
    for experience in experiences:
        starred_users = experience.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "tech_stack": experience.category,
                "project_url": "",
                "project_image_url": "",
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def show_experience(request):
    title_query = request.GET.get("title", "").strip()
    is_editor = request.user.groups.filter(name="Editor").exists() if request.user.is_authenticated else False

    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "title_query": title_query,
        "is_editor": is_editor,
        "form" : ExperienceForm(),
    }
    return render(request, "experience.html", context)

# function for starring feature exclusively for starred skills
@login_required(login_url="/login")
def toggle_skill_star(request,id):
    skill = get_object_or_404(Skill, pk=id)
    if request.method == "POST":
        if request.user in skill.starred_by.all():
            skill.starred_by.remove(request.user)
        else:
            skill.starred_by.add(request.user)
    return redirect("main:show_skills")

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Experience, pk=project_id)
    
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
            
    return redirect("main:show_experience")

@login_required(login_url="/login/")
def update_experience(request, project_id):
    if not (request.user.is_superuser or request.user.groups.filter(name="Editor").exists()):
        raise PermissionDenied

    project = get_object_or_404(Experience, pk=project_id)
    form = ExperienceForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience updated successfully!")
        return redirect("main:show_experience")

    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "form": form,
        "is_update": True,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/")
def delete_experience(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Experience, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Experience deleted successfully!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def get_skills_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.prefetch_related("starred_by").all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    data = []
    for skill in skills:
        starred_users = skill.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ",".join([u.username for u in starred_users])

        data.append({
            "pk": str(skill.id),
            "fields": {
                "name": skill.name,
                "description": skill.description or "",
                "logo_url": skill.logo_url or "",
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
    return JsonResponse(data,safe=False)

def show_skills(request):
    name_query = request.GET.get("name","").strip()
    is_editor = request.user.groups.filter(name="Editor").exist() if request.user.is_authenticated else False

    context = {
        "name": "Rebecca Love Lianov Simanjuntak",
        "title_query": name_query,
        "is_editor": is_editor,
        "form": SkillForm(),
    }
    return render(request, "skills.html", context)

# creating a new function : create_skill_ajax to suffice the project to send forms from model using fetch()
@require_POST
def create_skill_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message":"Only portofolio owner may create skill."}, status=403
        )

    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save()
        return JsonResponse(
            {"message":"Skill added successfully.","pk":str(skill.id)}, status=201
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login/")
def create_skill(request):
    """
    Handle the creation of a new Skill object using a ModelForm.
    If the request is POST and valid, saves the skill and redirects.
    """
    if not request.user.is_superuser:
        raise PermissionDenied

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

@login_required(login_url="/login/")
def update_skill(request, id):
    """
    Handle the modification of an existing Skill object using a ModelForm.
    If the request is POST and valid, updates the skill and redirects.
    """
    if not (request.user.is_superuser or request.user.groups.filter(name="Editor").exists()):
        raise PermissionDenied

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

@login_required(login_url="/login/")
def delete_skill(request, id):
    """
    Handle the deletion of an existing Skill object.
    Only allows deletion via POST requests for security.
    """
    if not request.user.is_superuser:
        raise PermissionDenied

    skill = get_object_or_404(Skill, pk=id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill deleted successfully!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")