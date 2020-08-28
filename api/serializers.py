from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {'passsword':{'write_only':True,'required':True}}
        def save(self):
            user = User(
                email=self.validated_data['email'],
                username = self.validated_data['username'],
            )
            password = self.validated_data['password']
            password2 = self.validated_data['password2']

            if password != password2:
                raise serializers.ValidationError({'password':'Password not match'})
            user.set_password(password)
            user.save()
            return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self,data):
        pass

# class EmployeeSerializer(serializers.ModelSerializer):
class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'url'
        )