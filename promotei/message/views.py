from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from message.models import Message



class MessageViewSet(viewsets.ViewSet):
    queryset = Message.object.all
    permission_classes = [IsAuthenticated]
   

    def list(self, request, *args, **kwargs):
        filtered_by_receiver = self.queryset.filter(receiver=request.user)
        serializer = Message(filtered_by_receiver, many=True)
        return Response(serializer.data)
    
    def retrieve(self,request, *args, **kwargs):
        pass