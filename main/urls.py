from django.urls import path

from main.views import (
    show_main, show_experience, create_experience, show_education, 
    get_experience_json, delete_experience, toggle_star, update_experience,
    show_skills, create_skill, update_skill, delete_skill, get_skills_json,
    register, login_user, logout_user
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("education/", show_education, name="show_education"),
    path("api/projects/", get_experience_json, name="get_experience_json"),
    path("projects/<uuid:project_id>/delete/", delete_experience, name="delete_experience"),
    path("projects/<uuid:project_id>/edit/", update_experience, name="update_experience"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),
    path("skills/", show_skills, name="show_skills"),
    path("skills/add/", create_skill, name="create_skill"),
    path("skills/<uuid:id>/edit/", update_skill, name="update_skill"),
    path("skills/<uuid:id>/delete/", delete_skill, name="delete_skill"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]