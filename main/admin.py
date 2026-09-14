from django.contrib import admin

# Register your models here.
from django.contrib import admin
from main.models import Experience, Education

admin.site.register(Experience)
admin.site.register(Education)
