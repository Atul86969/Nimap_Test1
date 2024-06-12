from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    client_id = serializers.PrimaryKeyRelatedField(source='client', queryset=Client.objects.all())

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client_id', 'users', 'created_at', 'created_by']

    def validate(self, data):
        client = data.get('client')
        
        if client:
            project_qs = Project.objects.filter(client=client)
            current_project = self.instance
            
            if current_project:
                project_qs = project_qs.exclude(id=current_project.id)
            
            if project_qs.exists():
                raise serializers.ValidationError("This client is already assigned to another project.")
        
        return data



class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']
