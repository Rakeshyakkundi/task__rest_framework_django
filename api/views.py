from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer,UserSerializer,EmployeeSerializer,LoginSerializer,EmployeeSerializer1,ProfileSearialiser
from .models import Task,Profile
from django.contrib.auth.models import User
from .forms import createuserform


from rest_framework import viewsets

from rest_framework.parsers import JSONParser

from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView

from rest_framework import generics,mixins

from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication

from rest_framework.permissions import IsAuthenticated,IsAdminUser

from django.contrib.auth import login,logout

from rest_framework.authtoken.models import Token
#authentication 1.basic  2.section  3.token
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
    authentication_classes = [SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)
    def post(self,request):
        return self.create(request)

    def put(self,request,id=None):
        check1 = str(self.request.user)
        obj = Task.objects.filter(id=id)
        for i in obj:
            check2 = str(i.created_by)
        if check1 == check2:
            return self.update(request,id)
        return JsonResponse({"result":"wrong user"})

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
        try:
            serializer = LoginSerializer(data=request.data)
            try:
                if serializer.is_valid():
                    try:
                        user = serializer.validated_data['user']
                        try:
                            login(request,user)
                            token,created = Token.objects.get_or_create(user=user)
                            return Response({'token':token.key},status=200)
                        except:
                            return Response({'result':'wrong credientials'})
                    except:
                        return Response({'result':'wrong username of password '})
                else:
                    return Response({'result':serializer.errors})
            except Exception as e:
                return Response({'result':e})
        except:
            return Response({'result':serializer.errors})

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    def post(self,request):
        logout(request)
        return Response(status=204)

#by using class we can do create  delete put POST methon in single class(default option)
#if u r using put u need to add /id/ in url  and even if u r using delete u should put /id/ in url 
# get /id/ in url also work
from rest_framework.decorators import action
from rest_framework.parsers import FormParser,MultiPartParser,JSONParser
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset =  User.objects.all()
    serializer_class = EmployeeSerializer
    parser_classes = (JSONParser,FormParser,MultiPartParser)

    @action(detail=True,methods=['put'])
    def profile(self,request,pk=None):
        user = self.get_object()
        profile = user.profile
        searialiser = ProfileSearialiser(profile,data=request.data)

        if searialiser.is_valid():
            searialiser.save()
            return Response(searialiser.data,status=200)
        else:
            return Response(searialiser.errors,status=400)

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