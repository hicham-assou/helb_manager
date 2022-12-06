from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Project

@receiver(post_save, sender=Project)
def createGroupCollaborator(sender, instance, created, **kwargs): #kwargs = eviter des argument supplementaire
    if created:
        Project.objects.create(project=instance)

@receiver(post_save, sender=Project)
def save_GroupCollaborator(sender, instance, **kwargs):
    instance.groupCollaborator.save()