from datetime import datetime

from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):

    PERIOD_DAYS = (
        (1, 'every day'),
        (2, 'every 2 day'),
        (3, 'every 3 day'),
        (4, 'every 4 day'),
        (5, 'every 5 day'),
        (6, 'every 6 day'),
        (7, 'every 7 day')
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='создатель привычки', **NULLABLE)

    place = models.CharField(
        max_length=100, **NULLABLE, verbose_name='место')

    time_do_it = models.DateTimeField(
        default=datetime.now, verbose_name='время делать это')

    action = models.CharField(
        max_length=150, verbose_name='действие', **NULLABLE)

    is_nice_habit = models.BooleanField(
        default=False, verbose_name='это приятная привычка?')

    related_habit = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        verbose_name='Связанная привычка', **NULLABLE)

    period = models.IntegerField(
        default=1, choices=PERIOD_DAYS,
        verbose_name='периодичность выполнения')

    prize = models.CharField(
        max_length=100, verbose_name='вознаграждение', **NULLABLE)

    time_to_complete = models.IntegerField(
        default=30, verbose_name='время выполнения (сек)')

    is_public = models.BooleanField(
        default=False, verbose_name='Опубликованная?')

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
