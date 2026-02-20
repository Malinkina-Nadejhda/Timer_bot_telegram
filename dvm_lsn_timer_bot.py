import ptbot
from pytimeparse import parse
import os
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify(chat_id, bot):
    bot.send_message(chat_id, "Время вышло")


def notify_progress(seconds_left, chat_id, bot, message_id, seconds):
    seconds_passed = seconds - seconds_left
    progress_bar = render_progressbar(seconds, seconds_passed)
    bot.update_message(chat_id, message_id, f"Осталось {seconds_left} секунд\n {progress_bar}")


def timer(chat_id, message, bot):
    seconds = parse(message)
    start_message = bot.send_message(chat_id, "Таймер запущен")
    message_id = start_message
    bot.create_countdown(seconds, notify_progress, bot=bot, chat_id=chat_id, message_id=message_id, seconds=seconds)
    bot.create_timer(seconds, notify, bot=bot, chat_id=chat_id)


def main():
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_TOKEN")
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(timer, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()

