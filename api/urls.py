from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import LoginView,LogoutView,EmployeeViewSet,TaskSerializerViewSet

from rest_framework import routers


router = routers.DefaultRouter()
router.register('employee',EmployeeViewSet)
router.register('employee-task',TaskSerializerViewSet)


urlpatterns = [
    path('', views.apiOverview,name="api-overview"),
    # path('auth/',obtain_auth_token),

    path('',include(router.urls)),

    path('task-class/',views.Task_class_view.as_view()),
    path('task-class/<int:pk>/',views.Task_class_detail.as_view()),
    path('task_list_view/',views.Task_list_view.as_view()),
    path('task_list_view/<int:id>/',views.Task_list_view.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('task-list/',views.taskList,name='task-list'),
    path('task-detail/<str:pk>/',views.taskDetail,name='task-detail'),
    path('task-create/',views.taskCreate,name='task-create'),
    path('task-update/<str:pk>/',views.taskUpdate,name='task-update'),
    path('task-delete/<str:pk>/',views.taskDelete,name='task-delete'),
    path('task-register/',views.RegisterUser,name='task-register'),
]
