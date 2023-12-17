from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Title')
    desc = models.TextField(max_length=500, verbose_name='Description', default='')
    amount = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}# {self.name}'
