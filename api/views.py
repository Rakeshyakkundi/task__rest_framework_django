from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer,UserSerializer,EmployeeSerializer,LoginSerializer
from .models import Task
from django.contrib.auth.models import User
from .forms import createuserform


from rest_framework import viewsets

from rest_framework.parsers import JSONParser

from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView

from rest_framework import generics,mixins
# Create your views here.

@api_view(['GET','POST'])
def apiOverview(request):
    api_urls = {
        'LIST':'/api/task-list/',
        'Detail View':'/api/task-detail/<str:pk>',
        'Create':'/api/task-create/',
        'Update':'/api/task-update/<str:pk>',
        'Delete':'/api/task-delete/<str:pk>',
        'Register':'/api/task-register/',
        'employee':'/api/task-register/employee/'
    }
    return Response(api_urls)

class Task_list_view(generics.GenericAPIView,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def get(self,request,id=None):
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)

    def perform_create(self, serializer):
        # serializer.save(created_by=self.request.user)
        serializer.save() 
    def perform_update(self, serializer):
        # serializer.save(created_by=self.request.user)
        serializer.save()

    def post(self,request):
        return self.create(request)

    def put(self,request,id=None):
        return self.update(request,id)

    def delete(self,request,id=None):
        return self.destroy(request,id)








# @api_view(['GET','POST'])
@csrf_exempt
def taskList(request):
    if request.method == "GET":
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks,many=True)
        return JsonResponse(serializer.data,safe=False)
        # return Response(serializer.data)
    if request.method == "POST":
        jason_parser = JSONParser()
        data = jason_parser.parse(request)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        else:
            return JsonResponse(serializer.errors,status=400)
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
        data1["success"]="deleted successful"
        return Response(data = data1)
    except:
        data1['error'] = "delete error"
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


class LoginView(APIView):
    def post(self,request):
        pass
    

class LogoutView(APIView):
    pass

#by using class we can do create  delete put POST methon in single class(default option)
#if u r using put u need to add /id/ in url  and even if u r using delete u should put /id/ in url
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset =  User.objects.all()
    serializer_class = EmployeeSerializer

class TaskSerializerViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


#class based view get,post,put,delete
class Task_class_view(APIView):
    def get(self,request):
        queryset = Task.objects.all()
        serializer_class = TaskSerializer(queryset,many=True)
        return Response(serializer_class.data,status=200)
    def post(self,request):
        data = request.data
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)

class Task_class_detail(APIView):
    def get_object(self,id):
        try:
            tasks = Task.objects.all().filter(id=id)
            return tasks
        except Exception as e:
            return Response({'error':'not found'},status=404)
    def get(self,request,pk=None):
        queryset = self.get_object(pk)
        serializer_class = TaskSerializer(queryset,many=True)
        return Response(serializer_class.data,status=200)

    def put(self,request,pk=None):
        task = self.get_object(pk)
        try:
            for i in task:
                k = i
            serializer = TaskSerializer(instance=k,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=200)
            else:
                return Response(serializer.errors,status=400)
        except:
            return Response({"error":"no"})
    def delete(self,request,pk=None):
        task = self.get_object(pk)
        for i in task:
            instance = i
        instance.delete()
        return Response({"success":"deleted successfully"},status=204)