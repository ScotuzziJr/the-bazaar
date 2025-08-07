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

class ProjectPost(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # normalmente será o criador
    content = models.TextField()
    image = models.ImageField(upload_to='project_posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # mais recentes primeiro

    def __str__(self):
        return f"Post de {self.author.username} em {self.project.title}"

class ProjectPostLike(models.Model):
    post = models.ForeignKey("ProjectPost", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "user")  # Evita duplicação

    def __str__(self):
        return f"{self.user.username} curtiu {self.post.id}"
    
class ProjectPostComment(models.Model):
    post = models.ForeignKey("ProjectPost", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comentário de {self.author.username} no post {self.post.id}"