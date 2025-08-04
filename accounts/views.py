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
