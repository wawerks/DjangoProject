from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatGroup, GroupMessage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GroupMessageSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = GroupMessage
        fields = ['id', 'group', 'author', 'body', 'created']
        read_only_fields = ['created']

class ChatGroupSerializer(serializers.ModelSerializer):
    chat_messages = GroupMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatGroup
        fields = ['id', 'group_name', 'chat_messages']