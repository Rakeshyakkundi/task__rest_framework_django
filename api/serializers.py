from rest_framework import serializers
from .models import Task,Profile
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
            # password2 = self.validated_data['password2']

            # if password != password2:
            #     raise serializers.ValidationError({'password':'Password not match'})
            user.set_password(password)
            user.save()
            return user


class ExceptionMessage(Exception):

    def passVal(self):
        data['result']="There is no such user"
        return self.data
    
    def passVal2(self):
        data = "User not exists with such credientials "
        return self.data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self,data):
        username = data.get("username","")
        password = data.get("password","")
        if username and password:
            user = authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data["user"]= user
                    return data
                else:
                    data['User']="user is not activated account .please check your mail"
                    return data
            else:
                data['result']="User not exists with such credientials "
                return data
        else:
            data['result']="There is no such user"
            return data


# class EmployeeSerializer(serializers.ModelSerializer):
class EmployeeSerializer1(serializers.HyperlinkedModelSerializer):
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

class ProfileSearialiser(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name','picture']



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'url',
            
        )
        write_only_fields = ('password',)
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user