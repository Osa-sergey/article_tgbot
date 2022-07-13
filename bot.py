import telebot

from controller.logic_layer import *
from settings.settings import TOKEN_STUDENT
from settings.text_settings import *

bot = telebot.TeleBot(TOKEN_STUDENT, parse_mode=None)
ll = LogicLayer(bot)


@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    ll.help_hint(chat_id)


@bot.message_handler(commands=['start'])
def start_command(message):
    msg = bot.send_message(message.chat.id, start_student)
    bot.register_next_step_handler(msg, ll.init_university_id_and_tags)


@bot.message_handler(commands=['student_number'])
def university_id_command(message):
    msg = bot.send_message(message.chat.id, student_number_student)
    bot.register_next_step_handler(msg, ll.save_university_id)


@bot.message_handler(commands=['tags'])
def tags_command(message):
    chat_id = message.chat.id
    markup = ll.create_categories_markup(chat_id)
    bot.send_message(chat_id, tags_student, reply_markup=markup)


@bot.message_handler(commands=['text'])
def create_or_replace_article_text(message):
    text = message.text[6:]
    chat_id = message.chat.id
    ll.create_or_edit_article(chat_id, text)


@bot.message_handler(content_types=['photo'])
def create_or_replace_article_with_img(message):
    text = message.caption
    img_id = message.photo[0].file_id
    chat_id = message.chat.id
    ll.create_or_edit_article(chat_id, text, img_id)


@bot.callback_query_handler(func=lambda call: not ll.is_admin_lambda(call))
def handle_keyboard(call):
    chat_id = call.message.chat.id
    text = call.data
    message_id = call.message.id
    ll.handle_keyboard(chat_id, text, message_id)


@bot.callback_query_handler(func=lambda call: ll.is_admin_lambda(call))
def handle_admin_keyboard(call):
    chat_id = call.message.chat.id
    text = call.data
    message_id = call.message.id
    ll.handle_admin_keyboard(chat_id, text, message_id)


bot.polling(none_stop=True, interval=0)
