from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from .models import Project, User, Task
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filter import Filter
from .forms import TaskForm

import random



# Create your views here.

def home(request):
    projects = Project.objects.all()
    filters = Filter(request.GET, queryset=projects)
    projects = filters.qs
    context = {
        'projects': projects,
        'filters': filters,
        'title': 'Home Page'
    }

    return render(request, 'manager_app/home.html', context)


def add_task(request, project_id):
    # Récupérer le projet à partir de la base de données
    project = Project.objects.get(pk=project_id)


    if request.method == 'POST':
        # Créer un formulaire lié aux données du formulaire
        form = TaskForm(request.POST, project=project)
        # Vérifier si le formulaire est valide
        if form.is_valid():
            # Enregistrer la tâche dans la base de données
            task = form.save(commit=False)
            task.project = project
            task.status_task = 'no status' #par defaut
            task.save()
            # Rediriger vers la page de détail du projet
            return redirect('project-detail', pk=project.pk)
    else:
        # Créer un formulaire vide
        form = TaskForm(project=project)
    # Rendre le formulaire
    return render(request, 'manager_app/add_task.html', {'form': form})


class ProjectListView(LoginRequiredMixin, ListView):  # affichage de tous les projets (home.html)
    model = Project
    template_name = 'manager_app/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'projects'



class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        #taches
        tasks = Task.objects.all()

        #collaborateur et users
        project = self.get_object()
        users = User.objects.values()
        status = project.status
        tabStatus = status.split(";")

        collaborators = project.collaborators

        context = super().get_context_data(**kwargs)
        context['tabStatus'] = tabStatus

        tabCollaborators = []
        cpt = 0
        for u in users:
            name = users[cpt]['username']
            if collaborators.find(name) != -1:
                tabCollaborators.append(name)
            cpt=cpt+1 # pour parcourir tt ma table user
        tabCollaborators.append(project.author.username)
        context['tabCollaborators'] = tabCollaborators
        context['users'] = users
        context['tasks'] = tasks

        colors = ["red", "green", "blue", "orange", "purple", "pink", "gray", "brown", "gold", "silver"]
        collaborator_colors = {}
        for collaborator in tabCollaborators:
            color = random.sample(colors, 1)[0]
            collaborator_colors[collaborator] = color
            colors.remove(color)

        context['collaborator_colors'] = collaborator_colors

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'content', 'status', 'collaborators']

    def form_valid(self, form): #communiquer l'auteur qui create le nouveau projet
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'content', 'status', 'collaborators']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): #peut pas modifier un projet qui n'est pas le sien
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False



    def form_valid(self, form):
        return super().form_valid(form)

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = '/'

    def test_func(self):  # peut pas modifier un projet qui n'est pas le sien
        project = self.get_object()
        if self.request.user == project.author:
            return True
        return False

def about(request):
    return render(request, 'manager_app/about.html')


