from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/new/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/complete/', views.mark_task_completed, name='mark_completed'),
    path('task/<int:pk>/pending/', views.mark_task_pending, name='mark_pending'),
]