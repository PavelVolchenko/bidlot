import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from accounts.models import CustomUser


def user_directory_path(instance, filename):
    return 'user-{0}-{1}/{2}'.format(
        instance.card.user_id,
        instance.card.user,
        filename)


class Card(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE)

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=128,
        blank=True)

    description = models.TextField(
        verbose_name='Подробное описание',
        blank=True)

    price = models.DecimalField(
        verbose_name='Стоимость',
        default=0,
        max_digits=10,
        decimal_places=2,
        blank=True)

    parsed_info = models.TextField(
        verbose_name='Полученное описание',
        blank=True)

    created = models.DateTimeField(
        auto_now_add=True)

    updated = models.DateTimeField(
        auto_now=True)

    is_active = models.BooleanField(
        default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('card_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        permissions = [
            ('special_status', 'Can be used'),
        ]


class Image(models.Model):
    path = models.ImageField(
        upload_to=user_directory_path)

    card = models.ForeignKey(
        Card,
        related_name='images',
        on_delete=models.CASCADE)

    created = models.DateTimeField(
        auto_now_add=True)

    updated = models.DateTimeField(
        auto_now=True)
