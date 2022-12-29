import django_filters
from django_filters import CharFilter

from .models import *
from django import template


class Filter(django_filters.FilterSet):
    title = CharFilter(field_name="title", lookup_expr='icontains')
    class Meta:
        model = Project
        fields = ['title']
        exclude = []

register = template.Library()

@register.filter
def color(collaborator):
    colors = {
        'collaborator1': 'red',
        'collaborator2': 'green',
        'collaborator3': 'blue',
    }
    return colors.get(collaborator, 'black')