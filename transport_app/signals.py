from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Traveler')
    Group.objects.get_or_create(name='Driver')
    Group.objects.get_or_create(name='Admin')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()