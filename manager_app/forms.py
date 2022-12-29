from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if self.project:
            #self.project.get_collaborators(self.project)
            self.fields['assign_to'] = forms.ChoiceField(choices=[(collaborator, collaborator) for collaborator in self.project.collaborators.split(';')])

    class Meta:
        model = Task
        fields = ['title_task', 'assign_to']

