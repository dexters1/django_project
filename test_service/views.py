from http.client import responses

from rest_framework.views import APIView

from .models import Task
from rest_framework import generics
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .celery_tasks import my_task
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserSerializer

class SignupView(APIView):
    http_method_names = ['post']
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_200_OK)


class LoginView(APIView):
    http_method_names = ['post']
    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response("missing user", status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})


class TestToken(APIView):
    http_method_names = ['get']
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response("passed!", status=status.HTTP_200_OK)


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