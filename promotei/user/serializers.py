from user.models import CustomUser, UserProfile
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from document.models import IdentityNumber
from rest_framework.generics import get_object_or_404


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'email' , 'indentity_number', 'role']
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source = 'user.id')
    phone_number = serializers.CharField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')
    role = serializers.CharField(source='user.role')
    indentity_number = serializers.CharField(source='indentity_number.indentity_number')
    first_name  = serializers.CharField(source='indentity_number.first_name')
    date_of_birth = serializers.CharField(source='indentity_number.date_of_birth')
    last_name = serializers.CharField(source='indentity_number.last_name')
    patronymic = serializers.CharField(source='indentity_number.patronymic')
    region = serializers.CharField(source='indentity_number.region')
    city = serializers.CharField(source='indentity_number.city')
    
    class Meta:
        model = UserProfile
        fields = [
                  'id',
                  'first_name',
                  'indentity_number', 
                  'first_name',
                  'role',
                  'email',
                  'phone_number',
                  'date_of_birth',
                  'last_name',
                  'patronymic',
                  'region',
                  'city'
                  ]


class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=12,
                                         validators=[
                                             RegexValidator(
                                                 regex=r"^\+?77(\d{9})$",
                                                 message=("Пожалуйста, введите корректный номер телефона")
                                             )])
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    role = serializers.CharField(max_length=30, write_only=True, required=True)
    indentity_number = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'password', 'password2', 'role', 'indentity_number')
        extra_kwargs = {'phone_number': {'write_only': True},
                        'password1': {'required': True},
                        'password2': {'required': True},
                        'email': {'required': True},
                        'indentity_number' : {'write_only': True},
                        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        user_identityNumber = get_object_or_404(IdentityNumber,indentity_number=attrs['indentity_number'])
        attrs['indentity_number'] = user_identityNumber
        try:
            user = CustomUser.objects.get(indentity_number=user_identityNumber)
            if user:
                isFound = True
        except:
            isFound = False
        if isFound:
            raise serializers.ValidationError({"user": "with this iin already exist"})
        else:
            return attrs
        
        
    def create(self, validated_data):
        user = CustomUser.objects.create(
            indentity_number=validated_data['indentity_number'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            role=validated_data['role'])
            
        user.set_password(validated_data['password'])
        user.save()
            
        UserProfile.objects.create(user=user, indentity_number=validated_data['indentity_number'])
    
        return user
        
        
class UserLoginSerializer(serializers.Serializer):
    email =  serializers.CharField(max_length=155, write_only=True, required=True)
    password = serializers.CharField(
        label=("Password"),
        trim_whitespace=False,
        write_only=True
    )
    
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email,
                                password=password)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserProrfileShortInfoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='user.id')
    phone_number = serializers.CharField(source='user.phone_number')
    email = serializers.EmailField(source='user.email')
    indentity_number = serializers.CharField(source='indentity_number.indentity_number')
    first_name  = serializers.CharField(source='indentity_number.first_name')
    last_name = serializers.CharField(source='indentity_number.last_name')
    
    class Meta:
        model = UserProfile
        fields = [
                  'id',
                  'first_name',
                  'indentity_number', 
                  'first_name',
                  'last_name',
                  'email',
                  'phone_number',
                  ]