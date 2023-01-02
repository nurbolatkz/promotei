
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from rest_framework.generics import get_object_or_404

from user.models import CustomUser, UserProfile
from document.models import IdentityNumber
from user.serializers import (UserLoginSerializer, UserProfileSerializer,
                              RegisterSerializer,  UserSerializer)



class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
        

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'Successfully registered user',
            'data': response.data
        })
    


class Logout(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # simply delete the token to force a login
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            Response('User is not autenticated')
            


class UserProfileViewSet(viewsets.ViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_instance(self):
        return UserProfile.objects.get(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = UserProfile.objects.all()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self,request, *args, **kwargs):
        if 'with' in request.query_params.keys():
            idendity_id = request.query_params['with']
            try:
                identityNumberobj = IdentityNumber.objects.get(indentity_number=idendity_id)
            except:
                return Response('User With this identityNumber does not exist', 404)
            instance = get_object_or_404(UserProfile,indentity_number=identityNumberobj)
            serializer =   UserProfileSerializer(instance)
        else:
            instance = self.get_instance()
            serializer = UserProfileSerializer(instance)
            
        return Response(serializer.data)
