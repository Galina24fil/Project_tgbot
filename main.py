# Импортируем необходимые классы.
import logging
import datetime
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from random import randint

# Запускаем логгирование
logging.basicConfig(filename='example.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
                    )

logger = logging.getLogger(__name__)

reply_keyboard_main = [['/tasks', '/statistics']]
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


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я бот-помощник для решения 25-ой задачи из ОГЭ по математике",
        reply_markup=markup_main
    )


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


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

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
