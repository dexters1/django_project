from .models import Task
from rest_framework import generics
from .serializers import TaskSerializer
from rest_framework.response import Response

class TaskList(generics.ListAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

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