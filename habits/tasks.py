import os
from datetime import datetime, timedelta
import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
import telebot

from habits.management.commands.bot import Command
from habits.models import Habit
from users.models import User

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
command = Command


@shared_task
def send_habit():
    # requests.post(
    url_send=f'https://api.telegram.org/bot6274986298:AAGCCkDZoA3vVQ7xi1esFnq09w5CxsfmaRc/sendMessage'
    # chat_id=849055520&text=privet')
    t_now = datetime.now().time()
    dt_now = datetime.now().date()
    users = User.objects.all()
    for user in users:
        habits = Habit.objects.filter(owner=user)
        for habit in habits:

            if dt_now == habit.date and t_now.strftime('%H:%M') == habit.time.strftime('%H:%M'):
                if habit.is_nice_habit:
                    text = f'Я буду {habit.action} в {habit.time} в {habit.place}'
                elif habit.related_habit:
                    text = (
                        f'Я буду {habit.action} в {habit.time} в {habit.place}. За эту полезную привычку сделаю приятную:'
                        f' {habit.related_habit}')
                elif habit.prize:
                    text = f'Я буду {habit.action} в {habit.time} в {habit.place}. Вознаграждение: {habit.prize}'

                params = {"chat_id": user.chat_id, "text": text}

                requests.post(url=url_send, params=params)
                habit.date += timedelta(days=habit.period)
                habit.save()

