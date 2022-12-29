from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from .models import Project, User, Task
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filter import Filter


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

class ProjectListView(LoginRequiredMixin, ListView):  # affichage de tous les projets (home.html)
    model = Project
    template_name = 'manager_app/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'projects'



class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        project = self.get_object()
        users = User.objects.values()
        print("model ==> ", users[0]['username'])
        status = project.status
        tabStatus = status.split(";")

        collaborators = project.collaborators

        context = super().get_context_data(**kwargs)
        context['tabStatus'] = tabStatus

        tabCollaborators = []
        print("inter ==> ",tabCollaborators)
        cpt = 0
        for u in users:
            name = users[cpt]['username']
            if collaborators.find(name) != -1:
                tabCollaborators.append(name)
            cpt=cpt+1 # pour parcourir tt ma table user
        context['tabCollaborators'] = tabCollaborators
        context['users'] = users
        return context



class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title_task', 'assign_to']

    def form_valid(self, form):
        #form.instance.project = self.request.project
        return super().form_valid(form) 


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


