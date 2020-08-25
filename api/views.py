from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer,UserSerializer
from .models import Task
from django.contrib.auth.models import User
from .forms import createuserform
# Create your views here.

@api_view(['GET','POST'])
def apiOverview(request):
    api_urls = {
        'LIST':'/api/task-list/',
        'Detail View':'/api/task-detail/<str:pk>',
        'Create':'/api/task-create/',
        'Update':'/api/task-update/<str:pk>',
        'Delete':'/api/task-delete/<str:pk>',
        'Register':'/api/task-register/'
    }
    return Response(api_urls)


@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request,pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks,many=False)
    return Response(serializer.data)

@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)
    try:
        if serializer.is_valid():
            serializer.save()
            return Response("task created")
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def taskUpdate(request,pk):
    tasks = Task.objects.get(id=pk)
    
    if request.method == "POST":
        serializer = TaskSerializer(instance=tasks,data=request.data)
        data1={}
        if serializer.is_valid():
            serializer.save()
            data1["success"]="update successful"
            return Response(data = data1)
        else:
            data1['error'] = "Update error"
            return Response(data=data1)
            # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def taskDelete(request,pk):
    data1 ={}
    try:
        tasks = Task.objects.get(id=pk)
        tasks.delete()
        data1["success"]="update successful"
        return Response(data = data1)
    except:
        data1['error'] = "Update error"
        return Response(data=data1)
    

@api_view(['POST'])
def RegisterUser(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response']='successfully registered new user'
        else:
            data = serializer.errors
    return Response(data)