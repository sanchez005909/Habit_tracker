import os
import telebot
from django.core.management import BaseCommand

from users.models import User

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "Добро пожаловать! Для получения привычек укажите свой email!")

    @bot.message_handler(content_types='text')
    def get_chat_id_for_user(massage):
        email = massage.text.strip()
        chat_id = massage.chat.id
        user = User.objects.filter(email=email).first()
        if user:
            bot.send_message(chat_id, 'Теперь вы будете получать напоминания о своих привычках!')
            user.chat_id = chat_id
            user.save()
        else:
            bot.send_message(chat_id, 'Такого пользователя не существует')
