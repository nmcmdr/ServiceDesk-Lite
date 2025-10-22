from rest_framework import serializers
from .models import Ticket, Comment
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'ticket', 'author', 'text', 'created_at')
        read_only_fields = ('ticket', 'author')

class TicketSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'description', 'status', 'created_at', 'updated_at', 'author', 'comments')
        read_only_fields = ('author', 'status') # Статус меняется только админом (если нужно)

class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'title', 'description', 'status')
        read_only_fields = ('id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Обычный пользователь не может менять статус
        if not self.context['request'].user.is_admin():
            self.fields.pop('status', None)