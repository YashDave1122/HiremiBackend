from django.contrib import admin

from .models import Education, Experience, SocialLink, Project

# Register your models here.
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(SocialLink)
admin.site.register(Project)