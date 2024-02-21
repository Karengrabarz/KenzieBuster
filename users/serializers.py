from rest_framework import serializers
from users.models import User


class UserSerializer ( serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField()
    email=  serializers.EmailField()
    password = serializers.CharField(write_only=True)
    birthdate = serializers.DateField(required=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField() 
    is_employee = serializers.BooleanField(required=False, allow_null=True)
    is_superuser = serializers.BooleanField(read_only=True)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already taken.")
        return value
    
    def create(self, validated_data: dict):
        is_employee = validated_data.get('is_employee', False)

        if not is_employee:
            validated_data['is_superuser'] = False
            user = User.objects.create_user(**validated_data)
        else:
            user = User.objects.create_superuser(**validated_data)
       
        user.set_password(validated_data['password'])
      
        return user
    
    def update(self, instance:User, validated_data:dict):
        for k,v in validated_data.items():
            setattr(instance,k,v)
            if k == 'password':
                instance.set_password(v)
        instance.save()
        return instance
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField()