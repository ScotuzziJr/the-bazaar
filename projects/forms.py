from django import forms
from .models import Project, CollaborationRole, ProjectJoinRequest, ProjectPost, ProjectPostComment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'repo_url', 'website_url', 'tags']

class CollaborationRoleForm(forms.ModelForm):
    class Meta:
        model = CollaborationRole
        fields = ['role', 'description']

class JoinRequestForm(forms.ModelForm):
    class Meta:
        model = ProjectJoinRequest
        fields = ['message']


class ProjectPostForm(forms.ModelForm):
    class Meta:
        model = ProjectPost
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Como anda o projeto?',
                'rows': 3,
                'class': 'form-control',
                'maxlength': 280
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }


class ProjectPostCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectPostComment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 2, "placeholder": "Escreva um comentário..."}),
        }