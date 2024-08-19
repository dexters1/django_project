from http.client import responses

from .models import Task
from rest_framework import generics
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import filters, status
from .celery_tasks import my_task

class TaskCelery(generics.RetrieveAPIView):
    def get(self, request):
        result = my_task.delay(3, 5)
        return Response({'Message': 'Celery task started', 'data': 1}, status=status.HTTP_201_CREATED)

class TaskList(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

class TaskUpdate(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    partial = True

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get']
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDelete(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(print("delete Task"))