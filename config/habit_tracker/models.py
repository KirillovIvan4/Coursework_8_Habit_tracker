from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from django import forms


NULLBLE = {"blank": True, "null": True}


class Days(models.Model):
    DAYS_OF_WEEK = (
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    )

    days = models.CharField(
        max_length=100,
        choices=DAYS_OF_WEEK,
        blank=True
    )
    def __str__(self):
        return f"{self.days}"

    class Meta:
        verbose_name = "день"
        verbose_name_plural = "дни"

class Habit(models.Model):
    place  = models.CharField(
        max_length=100,
        verbose_name='место выполнения привычки',
        help_text='введите место, в котором необходимо выполнять привычку'
    )
    time  = models.TimeField(
        verbose_name='время когда ее выполнять',
        help_text='введите время, когда необходимо выполнять привычку',
        **NULLBLE
    )
    action = models.TextField(
        verbose_name='что делать',
        help_text='введите действие, которое представляет собой привычка'
    )
    # frequency = models.PositiveIntegerField(
    #     default=1,
    #     validators=[MaxValueValidator(7)],
    #     verbose_name='периодичность привычки',
    #     help_text='введите периодичность выполнения привычки для напоминания в днях (по умолчанию ежедневная)'
    # )
    frequency = models.ManyToManyField(Days)

    time_to_perform = models.DurationField(
        verbose_name='время на выполнение привычки',
        validators=[MinValueValidator(timedelta(seconds=1)), MaxValueValidator(timedelta(seconds=120))],
        help_text='введите время, которое предположительно потратит пользователь на выполнение привычки',
    )
    publicity_indicator = models.BooleanField(
        default=False,
        verbose_name="признак публичности привычки",
        help_text='привычка опубликована в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки'
    )
    pleasant_habit_indicator =  models.BooleanField(
        default=False,
        verbose_name="признак приятной привычки",
        help_text='привычка, которую можно привязать к выполнению полезной привычки'
    )
    reward = models.CharField(
        max_length=150,
        verbose_name='вознаграждение',
        help_text='введите Вознаграждение которым пользователь должен себя вознаградить после выполнения привычки',
        **NULLBLE
    )
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name="связанная привычка",
        help_text='Привычка, которая связана с текущей (например, приятная привычка для вознаграждения)',
        **NULLBLE
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="habit_set",
        verbose_name="пользователь",
        **NULLBLE)

    def __str__(self):
        return f"{self.action} в {self.time} ({self.place})"

    def clean(self):
        """
        Проверяет, что заполнено только одно из полей:
        - reward (вознаграждение)
        - linked_habit (связанная привычка)
        - pleasant_habit_indicator (признак приятной привычки)
        """
        if self.reward and self.linked_habit:
            raise ValidationError(
                "Можно выбрать только одно: либо вознаграждение, либо связанную привычку!"
            )

        if not self.reward and not self.linked_habit and not self.pleasant_habit_indicator:
            raise ValidationError(
                "Укажите либо вознаграждение, либо связанную привычку, либо отметьте привычку как приятную!"
            )
        if self.reward and self.pleasant_habit_indicator:
            raise ValidationError(
                "Можно выбрать только одно: либо вознаграждение, либо отметку о привычке как приятной!"
            )
        if self.linked_habit and self.pleasant_habit_indicator:
            raise ValidationError(
                "Можно выбрать только одно: либо связанную привычку, либо отметку о привычке как приятной!"
            )

    def save(self, *args, **kwargs):
        # Вызываем валидацию перед сохранением
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"


