# Summary

This repository features code for a telegram bot that posts a reminder every Thursday at 11am EST
about the arrival of new free games in the Epic Games Store.

# Launching

```
python main.py --token=<your-bot-token> --chatid=<your-chat-id>
```

# Events

Events can be placed in the "events" folder.
They are formatted as in the following examples (timezones are given in pytz format):

```JSON
{
  "timezone": "US/Eastern",
  "hour": 11,
  "days": [
    "Thursday"
  ],
  "message": "Epic Games Store now has new free games"
}
```

```JSON
{
  "timezone": "US/Eastern",
  "hour": 13,
  "minute": 37,
  "second": 0,
  "days": [
    "Saturday",
    "Sunday"
  ],
  "message": "42!"
}
```

# Deployment

One (though perhaps not the best or most secure) way of deploying the bot on a Raspberry Pi is as follows:

- clone the repository to a location of your choice
- `python -m venv reminder`
- `source reminder/bin/activate`
- `pip install -r requirements.txt`
- store token and chat id as environment variables, if you want to manually launch the bot
- Add the bot as a cron job (`crontab -e`):
  - set CRON shell to bash: `SHELL=/bin/bash`
  - declare environment variables containing token and chat id (e.g. via `TOKEN=<token>`)
  - add job via `@reboot ~/path/to/repository/reminder/bin/python ~/path/to/main.py --token=$TOKEN --chatid=$CHATID --cron &>> /desired/path/to/xyz.log`
  - `--cron` simply adds a 30 second delay before starting the functional code execution, as cron starts before the network is available. Not a pretty fix, but a simple one.

# Links

https://github.com/python-telegram-bot/python-telegram-bot
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Builder-Pattern
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions---JobQueue
