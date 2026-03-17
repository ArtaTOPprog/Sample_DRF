# Определяет модели application для работы с БД
from django.db import models
from django.core.validators import MaxLengthValidator

class Note(models.Model):
    # Поля модели
    title = models.CharField(max_length=100, verbose_name='Заголовок', help_text='Введите заголовок заметки')
    content = models.TextField(validators=[MaxLengthValidator(10000)], verbose_name='Содержание', help_text='Введите содержание заметки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at'] # Сортировка по времени создания

        def __str__(self):
            # Возвращать строковое представление объекта
            return self.title[:50]
        
