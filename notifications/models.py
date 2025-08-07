from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('collab_request', 'Solicitação de Colaboração'),
        ('comment', 'Comentário'),
        ('like', 'Curtida'),
        ('new_post', 'Nova Postagem no Projeto'),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications'
    )
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    project = models.ForeignKey(
        'projects.Project', on_delete=models.CASCADE, null=True, blank=True
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.notification_type} -> {self.recipient.username}"
