from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.apiOverview,name="api-overview"),
    path('auth/',obtain_auth_token),
    path('task-list/',views.taskList,name='task-list'),
    path('task-detail/<str:pk>/',views.taskDetail,name='task-detail'),
    path('task-create/',views.taskCreate,name='task-create'),
    path('task-update/<str:pk>/',views.taskUpdate,name='task-update'),
    path('task-delete/<str:pk>/',views.taskDelete,name='task-delete'),
    path('task-register/',views.RegisterUser,name='task-register'),
]
