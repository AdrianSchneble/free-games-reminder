import sys

import pytz
from event_types.repeating import RepeatingEvent
import datetime as dt
import time
import argparse
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, JobQueue
import json
import os

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# TODO
# - event watcher
# - tests, once/if applicable/practical
# - differing prod and dev config (e.g. for event folder, launch message only in DEV environment, ...)

MAIN_CHANNEL_ID: str = ""
# TODO Chat class instead of just strings?
subscribed_chats: list[str] = []


### COMMANDS ###


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command."
    )


# TODO /subscribe
# TODO /unsubscribe
# TODO store chats as file

### CHANNEL MESSAGES ###


async def launch_message(context: ContextTypes.DEFAULT_TYPE):
    print("Launched!")
    await context.bot.send_message(chat_id=MAIN_CHANNEL_ID, text="Bot launched")


### GLOBAL MESSAGES ###


async def send_message(message, bot):
    print(f"Sending message: {message}")
    for chat in [MAIN_CHANNEL_ID, *subscribed_chats]:
        await bot.send_message(text=message, chat_id=chat)


async def send_repeating_event_message(context: ContextTypes.DEFAULT_TYPE):
    await send_message(context.job.data, context.bot)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Authentication token for the bot")
    parser.add_argument("--mainchannel", help="ID of main channel to send messages to")
    parser.add_argument(
        "--cron",
        help="Pass this boolean flag when launching the bot as a cronjob",
        action=argparse.BooleanOptionalAction,
    )
    args = parser.parse_args()
    token = args.token
    MAIN_CHANNEL_ID = args.mainchannel
    cron = args.cron
    if not token:
        sys.exit("Token required (pass via --token).")
    if not MAIN_CHANNEL_ID:
        sys.exit("Main channel ID required (pass via --mainchannel).")

    # When launching via cron @reboot, the network isn't yet available. To compensate, wait half a minute.
    # Not the prettiest solution, and there's probably a better way, but this is simple.
    if cron:
        print("Preparing for launch")
        time.sleep(30)

    print("Bot launching")

    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    job_queue: JobQueue = application.job_queue

    job_queue.run_once(launch_message, dt.timedelta(seconds=0))

    for subdir, dirs, files in os.walk("./events/repeating/"):
        for file in files:
            filepath = os.path.join(subdir, file)
            print(f"Joined: {filepath}")
            with open(filepath) as f:
                event: RepeatingEvent = json.load(f, object_hook=lambda data: RepeatingEvent(**data))
                job_queue.run_daily(
                    send_repeating_event_message,
                    data=event.message,
                    time=dt.time(
                        hour=event.hour,
                        minute=event.minute,
                        second=event.second,
                        tzinfo=pytz.timezone(event.timezone),
                    ),
                    days=tuple(event.days),
                )
                print(event)

    application.run_polling()
