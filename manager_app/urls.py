from django.urls import path
from . import views
from .views import ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView

urlpatterns = [
    path('', views.home, name = 'manager_app-home'), #localhost:8000/blog/
    path('about/', views.about, name = 'manager_app-about'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name = 'project-detail'),
    path('project/new/', ProjectCreateView.as_view(), name = 'project-create'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name = 'project-update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name = 'project-delete'),
    path('add_task/<int:project_id>/', views.add_task, name='add_task'),
    path('task/<int:project_id>/<int:task_id>/', views.status_task_update, name ='status_task_update'),
    path('task/<int:task_id>/delete_task/', views.delete_task, name = 'delete_task'),
    path('project/<int:project_id>/graphic_visualization/', views.graphic_visualization, name = 'graphic-visualization'),

]