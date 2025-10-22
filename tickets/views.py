from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket, Comment
from .serializers import TicketSerializer, CommentSerializer, TicketUpdateSerializer
from .permissions import IsAdminOrOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, filters, status

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('author').prefetch_related('comments').all()
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'status']

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TicketUpdateSerializer
        return TicketSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        ticket = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, ticket=ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Создание новой заявки",
        operation_description="Создает новую заявку в системе. Поле 'author' устанавливается автоматически на основе текущего пользователя.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'description'],
            properties={
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Заголовок заявки",
                    example="Не работает Wi-Fi"
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Подробное описание проблемы",
                    example="При подключении к сети устройство не получает IP-адрес."
                ),
            },
        )
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        ticket = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, ticket=ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='comments', url_name='ticket-comments')
    def list_comments(self, request, pk=None):
        ticket = self.get_object()
        comments = ticket.comments.all()
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)