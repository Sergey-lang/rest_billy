from django.db import models
from billy.models import Profile
from product.models import Product


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
