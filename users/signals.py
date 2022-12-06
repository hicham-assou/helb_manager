from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#creer un profile pour chaque utilisateur qui s'inscrit
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs): #kwargs = eviter des argument supplementaire
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
