from django.urls import path
from message.views import MessageViewSet

messageList = MessageViewSet.as_view({'get':'list'})

urlpatterns = [
    path('messages/', messageList, name='message'),
]