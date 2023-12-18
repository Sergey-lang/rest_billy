from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    PENDING = 'Pending'
    ACCEPT = 'Accept'
    FAILED = 'Failed'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPT, 'Accept'),
        (FAILED, 'Failed'),
    )

    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=20)

    def __str__(self):
        return f'id-{self.pk} {self.name}'
