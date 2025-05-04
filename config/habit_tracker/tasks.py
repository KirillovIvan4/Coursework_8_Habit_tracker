from config.settings import TELEGRAM_BOT_TOKEN
import requests
from datetime import datetime
from celery import shared_task

from users.models import User

@shared_task
def tg_massage_task():
    print("Задача запустилась")
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
                        params = {
                            'text': f'''Напоминаем у вас запланированна привычка
            Место выполнения привычки:{habit.place}
            Время когда ее выполнять:{habit.time}
            Что делать:{habit.action}
            Время на выполнение привычки:{habit.time_to_perform}
            Вознаграждение:{habit.reward}
            Связанная привычка:{habit.linked_habit}''',
                            'chat_id': chat_id
                        }
                        try:
                            response = requests.get(
                                f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
                                params=params
                            )
                            response.raise_for_status()
                            self.stdout.write(self.style.SUCCESS('Сообщение успешно отправлено'))
                        except requests.exceptions.RequestException as e:
                            self.stdout.write(self.style.ERROR(f'Ошибка при отправке сообщения: {e}'))
        else:
            print(f"У пользователя {user} не заполнен Tg chat id")