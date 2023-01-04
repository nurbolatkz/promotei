# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from message.models import Message
from rest_framework.decorators import action



class MessageViewSet(viewsets.ViewSet):
    queryset = Message.object.all
    permission_classes = [IsAuthenticated]
   

    def list(self, request, *args, **kwargs):
        filtered_by_receiver = self.queryset.filter(receiver=request.user)
        serializer = Message(filtered_by_receiver, many=True)
        return Response(serializer.data)
    
    def retrieve(self,request, *args, **kwargs):
        pass
    
    
    def create(self,request, *args, **kwargs):
        pass
    
    
    def delete(self,request, *args, **kwargs):
        pass
    
    def update(self,request, *args, **kwargs):
        pass
    
    @action(detail=True, methods=['get'])
    def set_read(self,request, *args, **kwargs):
        pass