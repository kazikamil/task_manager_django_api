from django.urls import path,include
from rest.views import *
urlpatterns = [
    path('project/',ProjectListCreateAPIView.as_view(),name='project'),
    path('project/update/<int:pk>',ProjectUpdateAPIView.as_view(),name='project_update'),
    path('task/',TaskListCreateAPIView.as_view(),name='task'),
    path('task/update/<int:pk>',TaskDeleteUpdateAPIView.as_view(),name='task_upt'),
    path('task/<int:task_id>/complete',CompleteTaskView.as_view(),name='complet'),
]