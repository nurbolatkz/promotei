from user.models import CustomUser, UserProfile
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'email', 'role' ]
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 
                  'indentity_number', 
                  'date_of_birth', 
                  'first_name', 
                  'last_name', 
                  'image' ]


class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=12,
                                         validators=[
                                             RegexValidator(
                                                 regex=r"^\+?77(\d{9})$",
                                                 message=("Пожалуйста, введите корректный номер телефона")
                                             )])
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'password', 'password2', 'role')
        extra_kwargs = {'phone_number': {'write_only': True},
                        'password1': {'required': True},
                        'password2': {'required': True},
                        'email': {'required': True},
                        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    def create(self, validated_data):
        user = CustomUser.objects.create(
            phone_number=validated_data['phone_number'],
            email=validated_data['email']
        )

        
        user.set_password(validated_data['password'])
        user.save()
        

        #user = CustomUser.objects.create_user(validated_data['email'], validated_data['password'])
        #user.set_password(validated_data['password'])
        #user.save()
        
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
    
    