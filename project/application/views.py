# Содержит представления для обработки запросов API

from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Note
from .serializers import *

class NoteListCreateView(generics.ListCreateAPIView):
    # Представление для списка и создания заметок
    queryset = Note.objects.all()
    

    def get_serializer(self):
        # Возвращает подходящий сериализатор в зависимости от запроса
        if self.request.method == 'POST':
            return NotCreateSerializer
        return NoteSerializer
    
    def get(self, request, *args, **kwargs):
        # Обрабатывает get запрос для получения списка заметок
        return super().get(request, *args, **kwargs)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()


    def get_serializer(self):
        if self.request.method in ['PUT', 'PATCH']:
            return NoteUpdateSerializer
        return NoteSerializer
    

    def update(self, request,  *args, **kwargs):
        # Обрабатывает обновление заметки
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_object(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Заметка успешно удалена'}, status=status.HTTP_204_NO_CONTENT)