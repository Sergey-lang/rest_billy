from django.db import models

from billy.models import Profile


class PointTransaction(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipient')
    points_count = models.PositiveIntegerField(verbose_name='Points count', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} {self.sender}--->{self.recipient} from {self.created_at}'
