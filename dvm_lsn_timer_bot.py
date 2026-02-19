import ptbot
from pytimeparse import parse
import os
from dotenv import load_dotenv


load_dotenv()

TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

bot = ptbot.Bot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify(chat_id):
    bot.send_message(chat_id, "Время вышло")


def notify_progress(seconds_left, chat_id, message_id, seconds):
    seconds_passed = seconds - seconds_left
    progress_bar = render_progressbar(seconds, seconds_passed)
    bot.update_message(chat_id, message_id, f"Осталось {seconds_left} секунд\n {progress_bar}")


def timer(chat_id, message):
    seconds = parse(message)
    start_message = bot.send_message(chat_id, "Таймер запущен")
    message_id = start_message
    bot.create_countdown(seconds, notify_progress, chat_id=chat_id, message_id=message_id, seconds=seconds)
    bot.create_timer(seconds, notify, chat_id=chat_id)


def main():
    bot.reply_on_message(timer)
    bot.run_bot()


if __name__ == '__main__':
    main()

    