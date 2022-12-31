
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from .models import Project, User, Task
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filter import Filter
from .forms import TaskForm

import random
import datetime
import json
from django.http import HttpResponse
# Create your views here.

# code Python
@csrf_exempt
def ma_vue(request, project_id, task_id):
    project = Project.objects.get(id=project_id)
    task = Task.objects.get(id=task_id)

    # Vérifiez que la requête est de type POST
    if request.method == "POST":
        data = json.loads(request.body)
        new_status = data["new_status"]

        #transformer les status en liste de status
        list_status = project.status.split(";")
        list_status.append('no status')
        for status in list_status:
            if status in new_status:
                new_status = status
        task.status_task = new_status
        task.save()
        project_chnology(project)

        return HttpResponse("Données reçues avec succès")
    else:
        print("qqlchose s'est mal passé ")

@csrf_exempt
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)

    # Vérifiez que la requête est de type POST
    if request.method == "POST":
        task.delete()
        return HttpResponse("Données reçues avec succès")
    else:
        print("qqlchose s'est mal passé ")

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

        tabStatus = []
        tabStatus.append('no status')
        tabStatus += status.split(";")


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


def getDates():
    list = []
    with open('D:\ecole\Q1-Q2-Q3-Q4\Q 3\web 2\project_chnology.txt', 'r') as f:
        for line in f:
            if '/' in line: #sa veut dire que cette ligne contient une date
                list.append(line.replace('\n', ''))
    return list


def getCountStatus(status, dates):
    list = []
    list_elem = []
    print("je suis la")
    with open('D:\ecole\Q1-Q2-Q3-Q4\Q 3\web 2\project_chnology.txt', 'r') as f:
        for line in f:
            for date in dates:
                day_found = False
                if date in line:
                    day_found = True
                    break
                else:
                    day_found = False

            if day_found == False:
                parts = line.split(':')
                number = int(parts[-1])
                print("nombre = ", number)
                list_elem.append(number)



    return list


def graphic_visualization(request, project_id):
    project = Project.objects.get(id=project_id)
    list_date = getDates()
    tabStatus = getStatus(project)
    list_count_for_status = getCountStatus(tabStatus, list_date)

    context = {
        'project': project,
        'status': tabStatus
    }
    return render(request, 'manager_app/graphic_visualization.html', context)


def getStatus(project):
    status = project.status
    tabStatus = []
    tabStatus.append('no status')
    tabStatus += status.split(";")
    return tabStatus


def project_chnology(project):

    #date
    now = datetime.datetime.now()
    date_string = now.strftime("%d/%m/%Y")

    #tasks
    tasks = Task.objects.all()

    #status
    tabStatus = getStatus(project)


    #traitement
    content = ""
    with open('D:\ecole\Q1-Q2-Q3-Q4\Q 3\web 2\project_chnology.txt', 'r') as f:
        for line in f:
            content += line
            if date_string in line:
                break



    with open('D:\ecole\Q1-Q2-Q3-Q4\Q 3\web 2\project_chnology.txt', 'w') as f:
        f.truncate()
        f.write(content)

        for status in tabStatus:
            #print("pour ", status)
            count = 0
            for task in tasks:
                if project == task.project:
                    if status == task.status_task:
                        count += 1
            f.write(status+':'+str(count)+'\n')