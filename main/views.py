from django.shortcuts import render

from main.models import Experience


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