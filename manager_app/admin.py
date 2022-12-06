from django.contrib import admin
from .models import Project, GroupOfCollaborators

# Register your models here.
admin.site.register(Project)
admin.site.register(GroupOfCollaborators)
