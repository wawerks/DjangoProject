from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import ChatGroup, GroupMessage
from .serializers import ChatGroupSerializer, GroupMessageSerializer

User = get_user_model()

class ChatViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'messages':
            return GroupMessage.objects.all()
        return ChatGroup.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'messages':
            return GroupMessageSerializer
        return ChatGroupSerializer

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        group = self.get_object()
        messages = GroupMessage.objects.filter(group=group)
        serializer = GroupMessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        group = self.get_object()
        serializer = GroupMessageSerializer(data={
            'group': group.id,
            'author': request.user.id,
            'body': request.data.get('content')
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
