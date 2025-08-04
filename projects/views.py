from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import Profile
from .models import Project, CollaborationRole, ProjectJoinRequest
from .forms import ProjectForm, JoinRequestForm

def project_list(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')

    tag_filter = request.GET.get('tag')
    if tag_filter:
        projects = Project.objects.filter(tags__icontains=tag_filter)
    else:
        projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    roles = CollaborationRole.objects.filter(project=project)
    tags = [t.strip() for t in project.tags.split(',')] if project.tags else []

    join_form = JoinRequestForm()

    # Lista de colaboradores aprovados
    collaborators = Profile.objects.filter(
        user__project_requests__project=project,
        user__project_requests__status='A'
    ).distinct()

    if request.method == 'POST':
        if request.user.is_authenticated:
            # Evitar duplicar solicitação pendente
            if not project.join_requests.filter(user=request.user, status='P').exists():
                join_form = JoinRequestForm(request.POST)
                if join_form.is_valid():
                    join_request = join_form.save(commit=False)
                    join_request.project = project
                    join_request.user = request.user
                    join_request.save()
        return redirect('project_detail', pk=pk)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'roles': roles,
        'tags': tags,
        'join_form': join_form,
        'collaborators': collaborators
    })

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_requests(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Apenas o criador pode gerenciar solicitações
    if project.creator != request.user:
        return redirect('project_detail', pk=pk)

    requests_qs = project.join_requests.all()

    if request.method == 'POST':
        req_id = request.POST.get('req_id')
        action = request.POST.get('action')
        join_request = get_object_or_404(ProjectJoinRequest, id=req_id, project=project)

        if action == 'approve':
            join_request.status = 'A'
        elif action == 'reject':
            join_request.status = 'R'
        join_request.save()

        return redirect('project_requests', pk=pk)

    return render(request, 'projects/project_requests.html', {
        'project': project,
        'requests': requests_qs
    })

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    # Garante que só o criador pode editar
    if project.creator != request.user:
        return redirect('project_detail', pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/project_form.html', {
        'form': form,
        'edit_mode': True
    })
