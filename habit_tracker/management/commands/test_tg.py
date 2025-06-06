from config.settings import TELEGRAM_BOT_TOKEN
import requests

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        params={
            'text': 'сообщение отправлено',
            'chat_id': 1976932412
        }
        try:
            response = requests.get(
                url=(
                    f'https://api.telegram.org/bot'
                    f'{TELEGRAM_BOT_TOKEN}/sendMessage'
            ),
                params=params
            )
            response.raise_for_status()
            self.stdout.write(
                self.style.SUCCESS('Сообщение успешно отправлено')
            )
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при отправке сообщения: {e}')
            )
