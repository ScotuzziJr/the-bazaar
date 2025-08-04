from django.contrib import admin
from django.urls import path
from projects import views as project_views
from accounts import views as account_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Projetos
    path('', project_views.project_list, name='project_list'),
    path('project/<int:pk>/', project_views.project_detail, name='project_detail'),
    path('project/new/', project_views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', project_views.project_edit, name='project_edit'),
    path('project/<int:pk>/requests/', project_views.project_requests, name='project_requests'),

    # Auth
    path('register/', account_views.register_view, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),

    # Perfil
    path('u/<str:username>/', account_views.profile_view, name='profile'),
    path('profile/edit/', account_views.edit_profile_view, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
