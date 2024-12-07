from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import ChatGroup, GroupMessage
from .serializers import UserSerializer, ChatGroupSerializer, GroupMessageSerializer
from django.conf import settings
from cryptography.fernet import Fernet
import json

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatGroupViewSet(viewsets.ModelViewSet):
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        group = self.get_object()
        message = request.data.get('message', '')
        
        # Create and save the message
        new_message = GroupMessage.objects.create(
            group=group,
            author=request.user,
            body=message
        )
        
        # Serialize the response
        serializer = GroupMessageSerializer(new_message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        group = self.get_object()
        messages = group.chat_messages.all()[:50]  # Get last 50 messages
        serializer = GroupMessageSerializer(messages, many=True)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GroupMessage.objects.filter(group__id=self.kwargs['group_pk'])

    def perform_create(self, serializer):
        group = ChatGroup.objects.get(id=self.kwargs['group_pk'])
        serializer.save(author=self.request.user, group=group)
