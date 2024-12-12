from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/%Y/%m/%d/', null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        # Force refresh from database to get latest value
        if hasattr(self, '_name_cache'):
            del self._name_cache
        return self.displayname if self.displayname else self.user.username

    @property
    def avatar(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return f'{settings.STATIC_URL}images/avatar.svg'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
