from django import forms
from .models import Task, SubTask
from .models import User

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        # collaborateur et admin du projet
        collaborators = self.project.collaborators
        tabCollaborators = []
        users = User.objects.values()
        cpt = 0
        for u in users:
            name = users[cpt]['username']
            if collaborators.find(name) != -1:
                tabCollaborators.append(name)
            cpt = cpt + 1  # pour parcourir tt ma table user
        tabCollaborators.append(self.project.author.username)#rajouter le createur du projet

        if self.project:
            collaborators = [(collaborator, collaborator) for collaborator in tabCollaborators]
            self.fields['assign_to'] = forms.ChoiceField(choices=collaborators)

    class Meta:
        model = Task
        fields = ['title_task', 'assign_to']

class SubTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        # collaborateur et admin du projet
        collaborators = self.project.collaborators
        tabCollaborators = []
        users = User.objects.values()
        cpt = 0
        for u in users:
            name = users[cpt]['username']
            if collaborators.find(name) != -1:
                tabCollaborators.append(name)
            cpt = cpt + 1  # pour parcourir tt ma table user
        tabCollaborators.append(self.project.author.username)#rajouter le createur du projet

        if self.project:
            collaborators = [(collaborator, collaborator) for collaborator in tabCollaborators]
            self.fields['assign_to'] = forms.ChoiceField(choices=collaborators)


    class Meta:
        model = SubTask
        fields = ['task','title_sub_task', 'assign_to']