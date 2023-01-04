from django.urls import path
from message.views import MessageViewSet

messageList = MessageViewSet.as_view({'get':'list'})

message_detail = MessageViewSet.as_view({'delete': 'destroy',
                                         "get": 'retrieve'})
messageMarkRead= MessageViewSet.as_view({'post': 'set_read'})

urlpatterns = [
    path('messages/', messageList, name='message'),
    path('messages/<str:message_id>', message_detail, name='message_detail'),
    path('messages/<str:message_id>/mark_read',messageMarkRead, name='mark_read'),
]