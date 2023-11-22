from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
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

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)

    REQUIRED_FIELDS = ["username", "email"]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Title')
    desc = models.TextField(max_length=500, verbose_name='Description', default='')
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}# {self.name}'


class PointTransaction(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipient')
    points_count = models.PositiveIntegerField(verbose_name='Points count', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}# {self.sender}--->{self.recipient}'
