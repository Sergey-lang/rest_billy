from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import Product


# https://stackoverflow.com/questions/11488974/django-create-user-profile-on-user-creation
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='First Name', default='')
    last_name = models.CharField(max_length=50, verbose_name='Last Name', default='')
    email = models.EmailField(unique=True, max_length=50)
    points = models.PositiveIntegerField(verbose_name='Points', default=0)
    received_points = models.PositiveIntegerField(verbose_name='Received Points', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    MANAGER = 1
    EMPLOYEE = 2
    ROLE_CHOICES = (
        (MANAGER, "Manager"),
        (EMPLOYEE, 'Employee'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=2)

    REQUIRED_FIELDS = ["first_name", "email"]

    def __str__(self):
        return f'# {self.user.pk}-{self.user.username}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, first_name=instance.username, email=instance.email, id=instance.pk)


class Order(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='creator')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')

    REQUIRED_FIELDS = ["product"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    PENDING = 'Pending'
    ACCEPT = 'Accept'
    DECLINED = 'Declined'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPT, 'Accept'),
        (DECLINED, 'Declined'),
    )

    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=20)

    def __str__(self):
        return f'id-{self.pk} {self.creator}'

