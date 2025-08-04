from django import forms
from .models import Project, CollaborationRole, ProjectJoinRequest

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
