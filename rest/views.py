from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import *
from .models import User,Project

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner== request.user
    
class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.project.owner)
        return obj.project.owner == request.user  # ✅ Vérifie si l'utilisateur est bien le propriétaire
   

class UserCreateAPIView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    serializer_class=ProjectSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)    
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else: print(serializer.errors)     
        

class ProjectUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user) 
    serializer_class=ProjectSerializer
    permission_classes=[IsOwner]


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)  # ✅ Retrieves only tasks from projects owned by the user

    def perform_create(self, serializer):
     project_id = self.kwargs.get("project_id") or self.request.query_params.get("project")

     if not project_id:
        raise serializers.ValidationError({"project": "L'ID du projet est requis dans l'URL ou les paramètres."})

     try:
        project = Project.objects.get(id=int(project_id))  # ✅ get() retourne UN SEUL objet
     except (ValueError, Project.DoesNotExist):
        raise serializers.ValidationError({"project": "Projet introuvable."})

     print(project.id)
     if project.owner != self.request.user:
        raise serializers.ValidationError({"project": "Vous ne pouvez pas créer une tâche pour ce projet."})

     serializer.save(project=project)



class TaskDeleteUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsProjectOwner]  # ✅ Les permissions sont vérifiées avant `get_queryset`

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)


# Create your views here.


