from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import ToDoSerializer, ToDoToggleCompleteSerializer
from todo.models import ToDo
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class ToDoListCreate(generics.ListCreateAPIView):
         serializer_class = ToDoSerializer
         permission_classes = [permissions.IsAuthenticated]

         def get_queryset(self):
             user = self.request.user
             print(self.request.user) 
             if user.is_authenticated:
                 return ToDo.objects.filter(user=user).order_by('-created')
             else:
                 return ToDo.objects.none()
             
         def perform_create(self, serializer):
             serializer.save(user=self.request.user)

class ToDoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
         serializer_class = ToDoSerializer
         permission_classes = [permissions.IsAuthenticated]

         def get_queryset(self):
             user = self.request.user
             if not user.is_authenticated:
                  return ToDo.objects.none()
             return ToDo.objects.filter(user=user).order_by('-created')
         
class ToDoToggleComplete(generics.UpdateAPIView):
         serializer_class = ToDoToggleCompleteSerializer
         permission_classes = [permissions.IsAuthenticated]

         def get_queryset(self):
             user = self.request.user
             if not user.is_authenticated:
                  return ToDo.objects.none()
             return ToDo.objects.filter(user=user).order_by('-created')

         def perform_update(self,serializer):
             serializer.instance.completed=not(serializer.instance.completed)
             serializer.save()

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'message': 'Usuario creado correctamente', 'token': token.key})
        except IntegrityError:
            return JsonResponse({'error': 'El nombre de usuario ya existe'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def login(request):
     if request.method == 'POST':
         data = JSONParser().parse(request)
         user = authenticate(
         request,
         username=data['username'],
         password=data['password'])
     if user is None:
         return JsonResponse(
             {'error':'unable to login. check username and password'}, status=400)
     else: # return user token
         try:
             token = Token.objects.get(user=user)
         except: # if token not in db, create a new one
             token = Token.objects.create(user=user)
         return JsonResponse({'token':str(token)}, status=201)
