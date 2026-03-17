from django.urls import path
from .views import NoteDetailView, NoteListCreateView

# Определяет url маршруты для application

app_name = 'application'

urlpatterns = [
    path('notes/', NoteListCreateView.as_view(), name='note_list_create'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
]