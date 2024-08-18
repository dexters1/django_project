from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'complete')
