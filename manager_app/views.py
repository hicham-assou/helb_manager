
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from pyexpat.errors import messages

from .models import Project, User, Task
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .filter import Filter
from .forms import TaskForm

import random
import datetime
import json
from django.http import HttpResponse
import matplotlib.pyplot as plt
# Create your views here.

# code Python
@csrf_exempt
def status_task_update(request, project_id, task_id):
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

        return HttpResponse("succes")
    else:
        print("something goes wrong ")

@csrf_exempt
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)

    # Vérifiez que la requête est de type POST
    if request.method == "POST":
        task.delete()
        return HttpResponse("succes")
    else:
        print("something goes wrong ")

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
            project_chnology(project)

            # Rediriger vers la page de détail du projet
            return redirect('project-detail', pk=project.pk)
    else:
        form = TaskForm(project=project)

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

        #colors = ["red", "green", "blue", "orange", "purple", "pink", "gray", "brown", "gold", "silver"]
        colors = ["green", "orange", "gold"]

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
        now = datetime.datetime.now()
        date_string = now.strftime("%d/%m/%Y")
        with open(form.instance.title+".txt", "w") as f: #creer un fichier pour chaque nouveau projet, sert a sauvegarder la chnologie du projet
            f.write(date_string)
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


def getDates(project):
    list = []
    with open(project.title+'.txt', 'r') as f:
        for line in f:
            if '/' in line: #sa veut dire que cette ligne contient une date
                list.append(line.replace('\n', ''))
    return list


def getCountStatus(project, status, dates):
    list = []
    list_elem = []
    with open(project.title + '.txt', 'r') as f:
        count = 0
        for line in f:
            for date in dates:
                day_found = False
                if date in line:
                    count+= 1
                    if count > 1:
                        list.append(list_elem)
                    list_elem = []
                    day_found = True
                    break
                else:
                    day_found = False

            if day_found == False:
                if line != '\n':
                    parts = line.split(':')
                    number = int(parts[-1])
                    list_elem.append(number)
        list.append(list_elem)
    return list

def graphic_visualization(request, project_id):
    project = Project.objects.get(id=project_id)
    list_date = getDates(project) # ['30/12/2022', '31/12/2022']
    print("dates", list_date)
    tabStatus = getStatus(project) # ['no status', 'to do', ' in progress', ' done']
    print("tabStatus", tabStatus)
    list_count_for_status = getCountStatus(project, tabStatus, list_date) # [[5, 4, 3, 2], [2, 2, 1, 1]]
    print("list_count_for_status", list_count_for_status)

    draw_graph(list_date, tabStatus, list_count_for_status)

    with open('graphic.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename='+project.title+'.pdf'
        return response

def draw_graph(dates, Status, count_for_status):
    # Créez une figure et un axe
    fig, ax = plt.subplots(figsize=(20, 10))
    # Utilisez la méthode bar pour créer des barres verticales
    # Spécifiez un intervalle entre les barres en utilisant le paramètre "width"
    bar_width = 0.2
    # Créez une boucle pour afficher les barres pour chaque date
    for i, date in enumerate(dates):
        ax.bar(Status, count_for_status[i], bar_width, label=date, align='edge')
        Status = [' ' + s for s in Status]
    # Ajoutez un titre et des étiquettes pour l'axe x et y
    plt.xticks(rotation=90)
    ax.set_title('progress of the project by day')
    ax.set_ylabel('Number of statuts')
    ax.set_xlabel('Statut')
    # Ajoutez une légende
    ax.legend()
    # Ajoutez cette ligne de code après avoir affiché le graphique
    plt.savefig('graphic.pdf')

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
    with open(project.title + '.txt', 'r') as f:
        for line in f:
            content += line
            if date_string in line:
                print("date trouvé")
                break
        print("contenu :", content)


    with open(project.title + '.txt', 'w') as f:
        f.truncate()
        f.write(content)

        for status in tabStatus:
            #print("pour ", status)
            count = 0
            for task in tasks:
                if project == task.project:
                    if status == task.status_task:
                        count += 1
            f.write('\n'+ status+':'+str(count))