from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Project(models.Model): #creation de la table projet dans la bd
    title = models.CharField(max_length=100) #titre de taille limité
    content = models.TextField()
    status = models.CharField(max_length=100)
    collaborators = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE ) #user par defaut, une entree dans la table users
                                                                # models.CASCADE : si user est supprimé alors tt ses projet seront supprime de la db

    def __str__(self): #redefinition de la methode toString (java)
        return self.title

         #redirect : rediriger vers une specifique route
         #reverse : retourne simplement l'url complet a cette route (un string)
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title_task = models.CharField(max_length=100)
    assign_to = models.CharField(max_length=100)
