from django.db import models
from datetime import datetime
from django.urls import reverse


# Опрееделяю класс для модели (БД), помечая тип полей, подробнее в документации
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Содержание')
    # blank позволяет оставлять пустую строчку, по умолчанию стоит False
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # auto_now_add - сокраняет один раз при объявлении, auto_now - постоянно обновляет при редактировании
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    # upload_to объявляет куда сохранять эти фотографии, /%Y/%m/%d/ разбивает файлы по дате загрузки
    is_published = models.BooleanField(default=True, verbose_name='Статус опубликованности')
    # default = True - в БД BooleanField показывает чекбоксы с галочками, если не указать значение по умолчанию(default), будет None
    category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT, verbose_name='Категория')

# маршрут для просмотра карточки
    def get_absolute_url(self):
        return reverse('new', kwargs={'new_id': self.pk})

# маршрут для юрл в шапке карточки на главной странице
    def url_to_categories(self):
        return reverse('category', kwargs={'category_id':self.category.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Category(models.Model):
    # db_index позволяет быстрее получать данные благодаря созданному индексу
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
