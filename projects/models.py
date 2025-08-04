from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    repo_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    tags = models.CharField(max_length=200, help_text="Separe por vírgulas")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CollaborationRole(models.Model):
    ROLE_CHOICES = [
        ('dev', 'Desenvolvedor'),
        ('designer', 'Designer'),
        ('pm', 'Produto'),
        ('other', 'Outro')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='roles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_role_display()} - {self.project.title}"

class ProjectJoinRequest(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('A', 'Aprovada'),
        ('R', 'Recusada'),
    ]

    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='join_requests'  # 👈 facilita consultas
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_requests'  # 👈 facilita consultas
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.project.title} ({self.get_status_display()})"
