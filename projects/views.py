from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from accounts.models import Profile
from .models import Project, CollaborationRole, ProjectJoinRequest, ProjectPost, ProjectPostLike
from .forms import CollaborationRoleForm, ProjectForm, JoinRequestForm, ProjectPostCommentForm, ProjectPostForm
from notifications.utils import create_notification

def projects_list(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    
    search_query = request.GET.get('search', '').strip()
    tag_filter = request.GET.get('tag', '').strip()

    projects = Project.objects.all()

    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if tag_filter:
        projects = projects.filter(tags__icontains=tag_filter)

    for project in projects:
        project.tag_list = [t.strip() for t in project.tags.split(',')] if project.tags else []

    return render(request, 'projects/project_list.html', {
        'projects': projects
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    roles = CollaborationRole.objects.filter(project=project)
    tags = [t.strip() for t in project.tags.split(',')] if project.tags else []

    posts = project.posts.select_related('author').all()

    join_form = JoinRequestForm()
    post_form = None

    if request.user == project.creator:
        post_form = ProjectPostForm()

    if request.method == 'POST':
        if 'create_post' in request.POST and request.user == project.creator:
            post_form = ProjectPostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.project = project
                post.author = request.user
                post.save()
                return redirect('project_detail', pk=pk)

        elif 'join_request' in request.POST and request.user.is_authenticated:
            join_form = JoinRequestForm(request.POST)
            if join_form.is_valid():
                exists = ProjectJoinRequest.objects.filter(
                    project=project,
                    user=request.user,
                    status='P'
                ).exists()
                if not exists:
                    join_request = join_form.save(commit=False)
                    join_request.project = project
                    join_request.user = request.user
                    join_request.save()

                    create_notification(
                        recipient=project.creator,
                        sender=request.user,
                        notification_type='collab_request',
                        project=project,
                        message=f"{request.user.username} quer colaborar no seu projeto '{project.title}'."
                    )
                    
                    return redirect('project_detail', pk=pk)

    collaborators = Profile.objects.filter(
        user__project_requests__project=project,
        user__project_requests__status='A'
    ).distinct()

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'roles': roles,
        'tags': tags,
        'join_form': join_form,
        'post_form': post_form,
        'posts': posts,
        'collaborators': collaborators,
    })

@login_required
def project_create(request):
    RoleFormSet = modelformset_factory(
        CollaborationRole,
        form=CollaborationRoleForm,
        extra=1,
        can_delete=False
    )

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        formset = RoleFormSet(request.POST, queryset=CollaborationRole.objects.none())

        if form.is_valid() and formset.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()

            roles = formset.save(commit=False)
            for role in roles:
                role.project = project
                role.save()

            return redirect('project_detail', pk=project.pk)

    else:
        form = ProjectForm()
        formset = RoleFormSet(queryset=CollaborationRole.objects.none())

    return render(request, 'projects/project_form.html', {
        'form': form,
        'formset': formset,
        'edit_mode': False
    })

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

    # Apenas o criador pode editar
    if project.creator != request.user:
        return redirect('project_detail', pk=pk)

    RoleFormSet = modelformset_factory(
        CollaborationRole,
        form=CollaborationRoleForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        formset = RoleFormSet(request.POST, queryset=project.roles.all())

        if form.is_valid() and formset.is_valid():
            form.save()
            roles = formset.save(commit=False)

            # Salvar roles
            for role in roles:
                role.project = project
                role.save()

            # Deletar roles marcados para exclusão
            for obj in formset.deleted_objects:
                obj.delete()

            return redirect('project_detail', pk=project.pk)

    else:
        form = ProjectForm(instance=project)
        formset = RoleFormSet(queryset=project.roles.all())

    return render(request, 'projects/project_form.html', {
        'form': form,
        'formset': formset,
        'edit_mode': True,
        'project': project
    })

def feed_view(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')

    posts = ProjectPost.objects.select_related('project', 'author').all()
    return render(request, 'feed.html', {'posts': posts})

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(ProjectPost, id=post_id)

    like, created = ProjectPostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": post.likes.count()
    })

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(ProjectPost, id=post_id)
    form = ProjectPostCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    return redirect(request.META.get("HTTP_REFERER", "feed"))
