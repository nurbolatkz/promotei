# Create your views here.
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from message.models import Message
from rest_framework.decorators import action
from message.serializers import MessageSerializer
from user.models import UserProfile


class MessageViewSet(viewsets.ViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    
    
    def get_instance(self):
        return UserProfile.objects.get(user=self.request.user)

    def list(self, request, *args, **kwargs):
        
        filtered_objects = list(self.queryset.filter(sender=self.get_instance()).order_by('-created_at'))
        filtered_objects += list(self.queryset.filter(receiver=self.get_instance()).order_by('-created_at'))
        
        serializer = MessageSerializer(filtered_objects, many=True)
        return Response(serializer.data)
    
    def retrieve(self,request, message_id=None, *args, **kwargs):
        if message_id is None:
            return Response({'Error': 'message id not provided'})
        try:
            message = self.queryset.get(pk=message_id, receiver=self.get_instance())
        except:
            return Response({'Error': 'Object does not exists'}, status=404)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #for_both_delete
    def destroy(self,request,message_id=None, *args, **kwargs):
        if message_id is None:
            return Response({'Error': 'message id not provided'})
        try:
            message = self.queryset.get(pk=message_id, receiver=self.get_instance())
        except:
            return Response({'Error': 'Object does not exists'}, status=404)
        
        message.delete()
        return Response({"Delete": 'Object deleted'}, status=status.HTTP_204_NO_CONTENT)
        

    @action(detail=True, methods=['get'])
    def set_read(self,request,message_id, *args, **kwargs):
        if message_id is None:
            return Response({'Error': 'message id not provided'})
        try:
            message = self.queryset.get(pk=message_id, receiver=self.get_instance())
        except:
            return Response({'Error': 'Object does not exists'}, status=404)
        message.is_read = True
        message.save()
        serializer = MessageSerializer(message)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
    def create(self,request, *args, **kwargs):
        pass
    
    def update(self,request, *args, **kwargs):
        pass