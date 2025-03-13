from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password']
        extra_kwargs={'password': {'write_only': True}}

    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        return user 
    

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','owner','name','date_start','date_end']
        extra_kwargs={'owner': {'read_only': True}}

    def create(self, validated_data):
        project=Project.objects.create(**validated_data)
        return project    
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['id','title','description','duration','project','owner','complete'] 
        extra_kwargs={'complete':{'read_only':True}}

    def create(self, validated_data):
        task=Task.objects.create(**validated_data)
        return task           
