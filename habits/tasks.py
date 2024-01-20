import os
from datetime import datetime, timedelta
import requests
from celery import shared_task
import telebot
from django.utils import timezone

from habits.models import Habit

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))


@shared_task
def send_habit():

    url_send = (f'https://api.telegram.org/bot'
                f'{os.getenv("TELEGRAM_BOT_TOKEN")}/sendMessage')
    dt_now = datetime.now().strftime('%y-%m-%d %H:%M')

    habits = Habit.objects.all()
    for habit in habits:
        time_do_it = (timezone.localtime(habit.time_do_it)
                      .strftime('%y-%m-%d %H:%M'))
        if dt_now == time_do_it:
            time = (timezone.localtime(habit.time_do_it).time()
                    .strftime('%H:%M'))
            if habit.is_nice_habit:
                text = (f'Я буду {habit.action} в {time} '
                        f'в {habit.place}')
            elif habit.related_habit:
                text = (
                    f'Я буду {habit.action} в {time} '
                    f'в {habit.place}. За эту полезную привычку, '
                    f'я сделаю приятную: {habit.related_habit}')
            elif habit.prize:
                text = (f'Я буду {habit.action} в {time} '
                        f'в {habit.place}. Вознаграждение: {habit.prize}')

            params = {"chat_id": habit.owner.chat_id, "text": text}

            requests.get(url=url_send, params=params)
            habit.time_do_it += timedelta(days=habit.period)
            habit.save()
