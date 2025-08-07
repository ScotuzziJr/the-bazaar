import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from projects.models import Project
from .forms import UserRegisterForm, ProfileForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Criar o usuário
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Login automático
            login(request, user)
            return redirect('project_list')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('project_list')
        else:
            return render(request, 'accounts/login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('project_list')

@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    
    # Projetos criados
    created_projects = Project.objects.filter(creator=user_obj)
    
    # Projetos que o usuário foi aprovado como colaborador
    collaborated_projects = Project.objects.filter(
        join_requests__user=user_obj,
        join_requests__status='A'
    ).distinct()

    return render(request, 'accounts/profile.html', {
        'profile_user': user_obj,
        'created_projects': created_projects,
        'collaborated_projects': collaborated_projects
    })

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect('project_list')
    return render(request, 'accounts/delete_account.html')

@login_required
def export_data_view(request):
    user = request.user
    profile = user.profile

    data = {
        "username": user.username,
        "email": user.email,
        "bio": profile.bio,
        "website": profile.website,
        "github": profile.github,
        "twitter": profile.twitter,
        "projects_created": [
            {
                "title": p.title,
                "description": p.description,
                "tags": p.tags
            }
            for p in user.project_set.all()
        ],
        "projects_collaborating": [
            {
                "title": req.project.title,
                "description": req.project.description,
                "tags": req.project.tags
            }
            for req in user.project_requests.filter(status='A')
        ]
    }

    response = HttpResponse(
        json.dumps(data, ensure_ascii=False, indent=4),
        content_type="application/json"
    )
    response['Content-Disposition'] = f'attachment; filename="{user.username}_data.json"'
    return response

def terms_view(request):
    return render(request, 'legal/terms.html')

def privacy_view(request):
    return render(request, 'legal/privacy.html')
