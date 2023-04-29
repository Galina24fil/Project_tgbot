# Импортируем необходимые классы.
import logging
import random
import json
import datetime
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, Bot
from random import randint
import requests


BOT_TOKEN = "6286692017:AAHlPoyRUzvUSaZuc6pHDX2x4BtB78hb3oY"
# Запускаем логгирование
logging.basicConfig(filename='example.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
                    )

logger = logging.getLogger(__name__)
# Супер-помощник ОГЭ

reply_keyboard_head = [['Русский'], ['Математика'], ['Физика'], ['Английский']]  # выбор предмета
markup_head = ReplyKeyboardMarkup(reply_keyboard_head, one_time_keyboard=False)

reply_keyboard_main = [['/tasks', '/statistics']]  # добавить тест теория и раздел
markup_main = ReplyKeyboardMarkup(reply_keyboard_main, one_time_keyboard=False)

reply_keyboard_tasks = [['/triangles'], ['/poligons'], ['/circles'], ['/combo'], ['/back']]
markup_tasks = ReplyKeyboardMarkup(reply_keyboard_tasks, one_time_keyboard=False)

reply_keyboard_statistics = [['/back']]
markup_statistics = ReplyKeyboardMarkup(reply_keyboard_statistics, one_time_keyboard=False)

reply_keyboard_triangles = [['/cancel']]
markup_triangles = ReplyKeyboardMarkup(reply_keyboard_triangles, one_time_keyboard=False)

reply_keyboard_poligons = [['/cancel']]
markup_poligons = ReplyKeyboardMarkup(reply_keyboard_poligons, one_time_keyboard=False)

reply_keyboard_circles = [['/cancel']]
markup_circles = ReplyKeyboardMarkup(reply_keyboard_circles, one_time_keyboard=False)

reply_keyboard_combo = [['/cancel']]
markup_combo = ReplyKeyboardMarkup(reply_keyboard_combo, one_time_keyboard=False)

reply_keyboard_rus = [['Задание 2'], ['Задание 3'], ['Задание 4'], ['Задание 5'], ['Обратно к предметам']]
markup_rus = ReplyKeyboardMarkup(reply_keyboard_rus, one_time_keyboard=False)

reply_keyboard_testrus3 = [['Пройти тест'], ['Немного теории'], ['Обратно в русский']]
markup_testrus3 = ReplyKeyboardMarkup(reply_keyboard_testrus3, one_time_keyboard=False)

reply_keyboard_stop = [['/stop']]
markup_stop = ReplyKeyboardMarkup(reply_keyboard_stop, one_time_keyboard=False)

reply_keyboard_eng = [['Правила письма'], ['Переводчик'], ['Обратно к предметам']]
markup_eng = ReplyKeyboardMarkup(reply_keyboard_eng, one_time_keyboard=False)

reply_keyboard = [['RU ->> EN', 'RU <<- EN'], ['Закончить перевод']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

reply_keyboard_physic = [['Механика'], ['МКТ'], ['Электричество'], ['Распады'], ['Обратно к предметам']]
markup_physic = ReplyKeyboardMarkup(reply_keyboard_physic, one_time_keyboard=False)

reply_keyboard_test_physic = [['Пройти тест'], ['Немного теории'], ['Обратно в физику']]
markup_test_physic = ReplyKeyboardMarkup(reply_keyboard_test_physic, one_time_keyboard=False)

reply_keyboard_maths = [['Задачи №25'], ['Немного теории'], ['Обратно к предметам']]
markup_maths = ReplyKeyboardMarkup(reply_keyboard_maths, one_time_keyboard=False)

reply_keyboard_tasks25 = [['Задачи №25'], ['Немного теории'], ['Обратно к предметам']]
markup_tasks25 = ReplyKeyboardMarkup(reply_keyboard_tasks25, one_time_keyboard=False)


async def login(update, context):
    pass


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот-помощник для подготовки к ОГЭ. Выбери предмет:",
        reply_markup=markup_head
    )
    return 1


async def subject(update, context):
    sub = update.message.text
    if sub == "Русский":
        await update.message.reply_text(
            "Вы зашли в раздел заданий по русскому языку", reply_markup=markup_rus)
        return 'rus'
    elif sub == 'Английский':
        await update.message.reply_text(
            "Вы зашли в раздел заданий по английскому языку", reply_markup=markup_eng)
        return 'eng'
    elif sub == "Физика":
        await update.message.reply_text(
            "Вы зашли в раздел заданий по физике", reply_markup=markup_physic)
        return 'phy'
    elif sub == "Математика":
        await update.message.reply_text(
            "Вы зашли в раздел заданий по математике", reply_markup=markup_maths)
        return 'maths'
    else:
        await update.message.reply_text(
            "Выберите нужный вам раздел с помощью кнопок", reply_markup=markup_head)
        return 1


async def download_rus_3(update, context):
    if update.message.text == 'Пройти тест':
        context.user_data['list'] = []
        context.user_data['count'] = 0
        with open(f'test_{context.user_data["file"]}.json', encoding="utf-8") as file:
            f = file.read()
            data = json.loads(f)
            data = data['test']
            ss = []
            for i in data:
                ss.append((i['question'], i['response'], i['help']))
        context.user_data['count'] = 0
        context.user_data['list'] = random.sample(ss, 5)

        print(context.user_data)
        await context.bot.send_message(update.message.chat_id, text=f"{context.user_data['list'][0][0]}",
                                       reply_markup=markup_stop, parse_mode='MarkdownV2')
        return 'test'
    elif update.message.text == 'Обратно в русский':
        await update.message.reply_text(
            "Вы вернулись в Великий и Могучий Русский язык!", reply_markup=markup_rus)
        return 'rus'
    elif update.message.text == 'Немного теории':
        doc = open(f'Теория{str(context.user_data["file"])[-1]}.pdf', 'rb')
        await context.bot.send_document(update.message.chat_id, doc)
        doc.close()


async def test(update, context):
    if update.message.text == context.user_data['list'][0][1]:
        context.user_data['count'] += 1
    answer = context.user_data['list'][0][1]
    help_prev = context.user_data['list'][0][2]
    context.user_data['list'].pop(0)
    if len(context.user_data['list']) != 0:
        first = f"Правильный ответ на предыдущий вопрос: {answer}\n"
        last = f"\n\n{context.user_data['list'][0][0]}"
        await context.bot.send_message(update.message.chat_id, text=f"{first}"
                                                                    f"||{help_prev}||"
                                                                    f"{last}", parse_mode='MarkdownV2')
        return 'test'
    else:
        await context.bot.send_message(update.message.chat_id,
                                       text=f"Правильных ответов было {context.user_data['count']}",
                                       reply_markup=markup_rus)
        context.user_data['count'] = 0
        context.user_data['list'] = []
        return 'rus'


async def rus3(update, context):
    sub = update.message.text
    if sub == "Задание 3":
        await update.message.reply_text(
            "Задание 3 ОГЭ по русскому", reply_markup=markup_testrus3)
        context.user_data["file"] = 'rus_3'
        return 'download'
    elif sub == "Задание 2":
        await update.message.reply_text(
            "Задание 2 ОГЭ по русскому", reply_markup=markup_testrus3)
        context.user_data["file"] = 'rus_2'
        return 'download'
    elif sub == "Задание 4":
        await update.message.reply_text(
            "Задание 4 ОГЭ по русскому", reply_markup=markup_testrus3)
        context.user_data["file"] = 'rus_4'
        return 'download'
    elif sub == "Задание 5":
        await update.message.reply_text(
            "Задание 5 ОГЭ по русскому", reply_markup=markup_testrus3)
        context.user_data["file"] = 'rus_5'
        return 'download'
    elif sub == 'Обратно к предметам':
        await update.message.reply_text(
            "Вы вернулись в главное меню", reply_markup=markup_head)
        return 1
    else:
        await update.message.reply_text(
            "Выберите нужный вам раздел с помощью кнопок", reply_markup=markup_rus)
        return 'rus'


async def eng(update, context):
    sub = update.message.text
    if sub == "Правила письма":
        await context.bot.send_photo(update.message.chat_id, 'shablon.jpg',
                                     caption="Шаблон письма ОГЭ\n P.S. это нужно выучить к 03.05 (группа ЕА)")
    elif sub == "Переводчик":
        await update.message.reply_text(
            "Выберите язык для перевода", reply_markup=markup)
        return 'trans'
    elif sub == 'Обратно к предметам':
        await update.message.reply_text(
            "Вы вернулись в главное меню", reply_markup=markup_head)
        return 1
    else:
        await update.message.reply_text(
            "Выберите нужный вам раздел с помощью кнопок", reply_markup=markup_rus)
        return 'rus'


async def change_lang(update, context):
    word = update.message.text
    if word == 'Закончить перевод':
        await update.message.reply_text(
            "Вы зашли в раздел заданий по английскому языку", reply_markup=markup_eng)
        return 'eng'
    elif word not in ['RU ->> EN', 'RU <<- EN']:
        if not context.user_data.get('lang') or context.user_data['lang'] == 0:
            await update.message.reply_text('Выберите на какой язык переводить:', reply_markup=reply_keyboard)
            return
        elif context.user_data['lang'] == 'RU ->> EN':
            body = {"targetLanguageCode": "en", "languageCode": "ru", "texts": word,
                    "folderId": FOLDER_ID}
            headers = {"Content-Type": "application/json", "Authorization": f"Api-Key {API_KEY}"}
            response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                     json=body, headers=headers)
            res = response.json()['translations'][0]['text']
        elif context.user_data['lang'] == 'RU <<- EN':
            body = {"targetLanguageCode": "ru", "languageCode": "en", "texts": word,
                    "folderId": FOLDER_ID}
            headers = {"Content-Type": "application/json", "Authorization": f"Api-Key {API_KEY}"}
            response = requests.post(
                'https://translate.api.cloud.yandex.net/translate/v2/translate',
                json=body, headers=headers)
            res = response.json()['translations'][0]['text']
        await update.message.reply_text(f'Переведенное слово:\n{res}')
    else:
        context.user_data['lang'] = word
        await update.message.reply_text(f'Язык изменен на: {word}.')


async def download_physic(update, context):
    if update.message.text == 'Пройти тест':
        context.user_data['list'] = []
        context.user_data['count'] = 0
        with open(f'test_{context.user_data["file"]}.json', encoding="utf-8") as file:
            f = file.read()
            data = json.loads(f)
            data = data['test']
            ss = []
            for i in data:
                ss.append((i['question'], i['response'], i['help']))
        context.user_data['count'] = 0
        context.user_data['list'] = random.sample(ss, 5)

        print(context.user_data)
        await context.bot.send_message(update.message.chat_id, text=f"{context.user_data['list'][0][0]}",
                                       reply_markup=markup_stop, parse_mode='MarkdownV2')
        return 'test_phy'
    elif update.message.text == 'Обратно в физику':
        await update.message.reply_text(
            "Вы вернулись", reply_markup=markup_physic)
        return 'phy'
    elif update.message.text == 'Немного теории':
        doc = open(f'Теор{str(context.user_data["file"])[-1]}.pdf', 'rb')
        await context.bot.send_document(update.message.chat_id, doc)
        doc.close()


async def test_physic(update, context):
    if update.message.text == context.user_data['list'][0][1]:
        context.user_data['count'] += 1
    answer = context.user_data['list'][0][1]
    help_prev = context.user_data['list'][0][2]
    context.user_data['list'].pop(0)
    if len(context.user_data['list']) != 0:
        first = f"Правильный ответ на предыдущий вопрос: {answer}\n"
        last = f"\n\n{context.user_data['list'][0][0]}"
        await context.bot.send_message(update.message.chat_id, text=f"{first}"
                                                                    f"||{help_prev}||"
                                                                    f"{last}", parse_mode='MarkdownV2')
        return 'test_phy'
    else:
        first = f"Правильный ответ на предыдущий вопрос: {answer}\n"
        await context.bot.send_message(update.message.chat_id,
                                       text=f"{first}"
                                            f"||{help_prev}||"
                                            f"\nПравильных ответов было {context.user_data['count']}",
                                       reply_markup=markup_physic, parse_mode='MarkdownV2')
        context.user_data['count'] = 0
        context.user_data['list'] = []
        return 'phy'


async def physic(update, context):
    sub = update.message.text
    if sub == "Механика":
        await update.message.reply_text(
            "Раздел механика", reply_markup=markup_test_physic)
        context.user_data["file"] = '1'
        return 'download_physic'
    elif sub == "МКТ":
        await update.message.reply_text(
            "Раздел МКТ", reply_markup=markup_test_physic)
        context.user_data["file"] = '2'
        return 'download_physic'
    elif sub == "Электричество":
        await update.message.reply_text(
            "Раздел электричество", reply_markup=markup_test_physic)
        context.user_data["file"] = '3'
        return 'download_physic'
    elif sub == "Распады":
        await update.message.reply_text(
            "Раздел распады", reply_markup=markup_test_physic)
        context.user_data["file"] = '4'
        return 'download_physic'
    elif sub == 'Обратно к предметам':
        await update.message.reply_text(
            "Вы вернулись в главное меню", reply_markup=markup_head)
        return 1
    else:
        await update.message.reply_text(
            "Выберите нужный вам раздел с помощью кнопок", reply_markup=markup_physic)
        return 'phy'


async def maths(update, context):
    sub = update.message.text
    if sub == "Задачи №25":
        mathss = ['maths1.jpg', 'maths2.jpg', 'maths3.jpg', 'maths4.jpg', 'maths5.jpg', 'maths6.jpg']
        m = random.sample(mathss, 1)[0]
        await context.bot.send_photo(update.message.chat_id, m,
                                     caption=f"Задачи №25 ({m[-5]})")
    elif sub == "Немного теории":
        doc = open(f'Зачет по геометрии(1-5стр).pdf', 'rb')
        await context.bot.send_document(update.message.chat_id, doc)
        doc.close()
    elif sub == 'Обратно к предметам':
        await update.message.reply_text(
            "Вы вернулись в главное меню", reply_markup=markup_head)
        return 1
    else:
        await update.message.reply_text(
            "Выберите нужный вам раздел с помощью кнопок", reply_markup=markup_maths)
        return 'maths'


async def help_command(update, context):
    await update.message.reply_text("Вот, что я умею:\n"
                                    "/tasks - меню тем\n"
                                    "/statistics - статистика решенных задач\n"
                                    "/triangles - задачи на треугольники\n"
                                    "/poligons - задачи на многоугольники\n"
                                    "/circles - задачи на окружности\n"
                                    "/combo - задачи на комбинацию тем\n"
                                    "/back - возврат в основное меню (задач и статистики)\n"
                                    "/cancel - возврат в меню с темами задач")


async def echo(update, context):
    await update.message.reply_text(f"Я получил сообщение: '{update.message.text}'")


async def tasks(update, context):
    await update.message.reply_text(
        "Вы зашли в раздел /tasks", reply_markup=markup_tasks)


async def triangles(update, context):
    await update.message.reply_text(
        "Вы зашли в раздел /triangles , выберите одну из задач", reply_markup=markup_triangles)


async def poligons(update, context):
    await update.message.reply_text(
        "Вы зашли в раздел /poligons , выберите одну из задач", reply_markup=markup_poligons)


async def circles(update, context):
    await update.message.reply_text(
        "Вы зашли в раздел /circles , выберите одну из задач", reply_markup=markup_circles)


async def combo(update, context):
    await update.message.reply_text(
        "Вы зашли в раздел /combo , выберите одну из задач", reply_markup=markup_combo)


async def cancel(update, context):
    await update.message.reply_text(
        "Вы вернулись в меню с темами задач", reply_markup=markup_tasks)


async def statistics(update, context):
    await update.message.reply_text(
        "Вы зашли в раздел /statistics", reply_markup=markup_statistics)


async def back(update, context):
    await update.message.reply_text(
        "Вы вернулись в основное меню", reply_markup=markup_main)


async def stop(update, context):
    await update.message.reply_text(f"Спасибо за прохождение теста\n"
                                    f"Правильных ответов: {context.user_data['count']}", reply_markup=markup_head)
    context.user_data['count'] = 0

    return 1


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, subject)],
            'rus': [MessageHandler(filters.TEXT & ~filters.COMMAND, rus3)],
            'download': [MessageHandler(filters.TEXT & ~filters.COMMAND, download_rus_3)],
            'test': [MessageHandler(filters.TEXT & ~filters.COMMAND, test)],
            'eng': [MessageHandler(filters.TEXT & ~filters.COMMAND, eng)],
            'trans': [MessageHandler(filters.TEXT & ~filters.COMMAND, change_lang)],
            'phy': [MessageHandler(filters.TEXT & ~filters.COMMAND, physic)],
            'download_physic': [MessageHandler(filters.TEXT & ~filters.COMMAND, download_physic)],
            'test_phy': [MessageHandler(filters.TEXT & ~filters.COMMAND, test_physic)],
            'maths': [MessageHandler(filters.TEXT & ~filters.COMMAND, maths)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)

    application.add_handler(text_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tasks", tasks))
    application.add_handler(CommandHandler("triangles", triangles))
    application.add_handler(CommandHandler("poligons", poligons))
    application.add_handler(CommandHandler("circles", circles))
    application.add_handler(CommandHandler("combo", combo))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("statistics", statistics))
    application.add_handler(CommandHandler("back", back))

    application.run_polling()


if __name__ == '__main__':
    main()
