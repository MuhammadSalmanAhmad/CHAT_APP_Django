from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response  # Import Response class
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny  # Import AllowAny class
from .serializers import UserSerializer
from rest_framework.decorators import action

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[AllowAny]
    @action(methods=['GET'],detail=False)
    def get_users_list(self,request):
        queryset=User.objects.all()
        serializer=UserSerializer(queryset,many=True)
        
        return Response(serializer.data)
    
    @action(methods=['post'],detail=False)
    def create_user(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user created successfully"},status=201)
        return Response(serializer.errors,status=400)