import os
from datetime import datetime, timedelta
import requests
from celery import shared_task
import telebot

from habits.models import Habit
from users.models import User

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

@shared_task
def send_habit():

    url_send = (f'https://api.telegram.org/bot'
                f'{os.getenv("TELEGRAM_BOT_TOKEN")}/sendMessage')
    dt_now = datetime.now().strftime('%y-%m-%d %H:%M')

    users = User.objects.all()
    for user in users:
        habits = Habit.objects.filter(owner=user)
        for habit in habits:
            time_do_it = habit.time_do_it.strftime('%y-%m-%d %H:%M')
            if dt_now == time_do_it:
                if habit.is_nice_habit:
                    text = (f'Я буду {habit.action} в {habit.time_do_it} '
                            f'в {habit.place}')
                elif habit.related_habit:
                    text = (
                        f'Я буду {habit.action} в {habit.time_do_it} '
                        f'в {habit.place}. За эту полезную привычку, '
                        f'я сделаю приятную: {habit.related_habit}')
                elif habit.prize:
                    text = (f'Я буду {habit.action} в {habit.time_do_it} '
                            f'в {habit.place}. Вознаграждение: {habit.prize}')

                params = {"chat_id": user.chat_id, "text": text}

                requests.post(url=url_send, params=params)
                habit.date += timedelta(days=habit.period)
                habit.save()

