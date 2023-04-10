import asyncio
import sys
import telegram
import datetime
import pytz
import time
import argparse

# Set the time zone to Eastern Standard Time (EST)
tz = pytz.timezone("America/New_York")


async def main(token, chat_id):
    bot = telegram.Bot(token)
    async with bot:
        await bot.send_message(text="Reminder: Epic Games Store now has new free games :)", chat_id=chat_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="authentication token")
    parser.add_argument("--chatid", help="chat id")
    parser.add_argument("--cron", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    token = args.token
    chat_id = args.chatid
    cron = args.cron
    if not token:
        sys.exit("Token required (pass via --token).")
    if not chat_id:
        sys.exit("Chat ID required (pass via --chatid).")

    # When launching via cron @reboot, the network isn't yet available. To compensate, wait half a minute.
    # Not the prettiest solution, and there's probably a better way, but this is simple.
    if cron:
        time.sleep(30)

    print("Launching telegram bot")

    while True:
        now = datetime.datetime.now(tz)
        # Thursday, 11am EST
        if now.weekday() == 3 and now.hour == 11:
            print("Sending message")
            asyncio.run(main(token, chat_id))
            time.sleep(60 * 60)  # Wait for one hour before checking again
        else:
            time.sleep(60)  # Wait for one minute before checking again
