from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='First Name', default='')
    last_name = models.CharField(max_length=50, verbose_name='Last Name', default='')
    points = models.PositiveIntegerField(verbose_name='Points', default=0)
    received_points = models.PositiveIntegerField(verbose_name='Received Points', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Title')
    desc = models.TextField(max_length=500, verbose_name='Description', default='')
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#{self.pk}-{self.name}'
