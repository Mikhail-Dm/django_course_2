import pytz
from django.conf import settings

from django.db import models
from django.db.models.signals import post_save, post_delete
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='аватар')
    avatar_url = models.CharField(max_length=128, blank=True, null=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)

    activate_key = models.CharField(max_length=128, blank=True, null=True, verbose_name='Ключ активации')
    activate_key_expired = models.DateTimeField(blank=True, null=True)

    def is_activate_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activate_key_expired + timedelta(hours=48):
            return True
        return False

    def activate_user(self):
        self.is_active = True
        self.activate_key = None
        self.is_activate_key_expired = None
        self.save()


class ShopUserProfile(models.Model):
    MALE = 'М'
    FEMALE = 'Ж'
    OTHERS = 'И'

    GENDER = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
        (OTHERS, 'Иное'),
    )

    user = models.OneToOneField(ShopUser, db_index=True, null=True, unique=True, on_delete=models.CASCADE)
    tagline = models.CharField(blank=True, max_length=128, verbose_name='Тэги')
    about_me = models.TextField(verbose_name='обо мне')
    gender = models.CharField(choices=GENDER, max_length=1, default=OTHERS, verbose_name='Пол')

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def update_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
