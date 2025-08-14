from django.contrib import admin
from django.urls import path, re_path
from projects import views as project_views
from accounts import views as account_views
from notifications import views as notification_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    
    # Projetos
    path('', project_views.feed_view, name='feed'),
    path('projects/', project_views.projects_list, name='project_list'),
    path('project/<int:pk>/', project_views.project_detail, name='project_detail'),
    path('project/new/', project_views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', project_views.project_edit, name='project_edit'),
    path('project/<int:pk>/requests/', project_views.project_requests, name='project_requests'),
    path("post/<int:post_id>/like/", project_views.toggle_like, name="toggle_like"),
    path("post/<int:post_id>/comment/", project_views.add_comment, name="add_comment"),
    
    # Auth
    path('register/', account_views.register_view, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),

    # Perfil
    path('u/<str:username>/', account_views.profile_view, name='profile'),
    path('profile/edit/', account_views.edit_profile_view, name='edit_profile'),

    # Compliance
    path('delete-account/', account_views.delete_account_view, name='delete_account'),
    path('export-data/', account_views.export_data_view, name='export_data'), 
    path('terms/', account_views.terms_view, name='terms'),
    path('privacy/', account_views.privacy_view, name='privacy'),

    path('notifications/', notification_views.notifications_list, name='notifications_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
