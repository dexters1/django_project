from django.urls import path
from rest_framework.schemas import get_schema_view
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete


urlpatterns = [
    path('api_schema/', get_schema_view(title='API Schema', description='Guide for the REST API'), name='api-schema'),
    path('tasks/', TaskList.as_view(), name='tasks'),
    path('task/<str:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<str:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<str:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/schema/', SpectacularSwaggerView.as_view(url_name="schema")),
]