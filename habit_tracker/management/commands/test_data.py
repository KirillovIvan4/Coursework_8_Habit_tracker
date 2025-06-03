from config.settings import TELEGRAM_BOT_TOKEN
import requests
from django.core.management.base import BaseCommand
from datetime import datetime

from habit_tracker.models import Habit
from users.models import User


class Command(BaseCommand):
    """Команда для отправки напоминаний о привычках через Telegram."""

    def handle(self, *args, **options):
        """Основной метод обработки команды."""
        now = datetime.now()
        days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        all_users = User.objects.all()

        for user in all_users:
            chat_id = user.tg_chat_id
            if chat_id:
                user_all_habits = user.habit_set.all()
                for habit in user_all_habits:
                    for frequency in habit.frequency.all():
                        if frequency.days == days_of_week[now.weekday()]:
                            message_text = (
                                f"Напоминаем у вас запланирована привычка\n"
                                f"Место выполнения привычки: {habit.place}\n"
                                f"Время когда ее выполнять: {habit.time}\n"
                                f"Что делать: {habit.action}\n"
                                f"Время на выполнение: {habit.time_to_perform}\n"
                                f"Вознаграждение: {habit.reward}\n"
                                f"Связанная привычка: {habit.linked_habit}"
                            )

                            params = {
                                'text': message_text,
                                'chat_id': chat_id
                            }

                            try:
                                response = requests.get(
                                    f'https://api.telegram.org/bot'
                                    f'{TELEGRAM_BOT_TOKEN}/sendMessage',
                                    params=params
                                )
                                response.raise_for_status()
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        'Сообщение успешно отправлено'
                                    )
                                )
                            except requests.exceptions.RequestException as e:
                                self.stdout.write(
                                    self.style.ERROR(
                                        f'Ошибка при отправке сообщения: {e}'
                                    )
                                )
