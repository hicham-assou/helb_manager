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

]