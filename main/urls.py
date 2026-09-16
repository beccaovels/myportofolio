from django.urls import path

from main.views import show_main, show_experience, create_experience,show_education

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("education/", show_education, name="show_education"),
]