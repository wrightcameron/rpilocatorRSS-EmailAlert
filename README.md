# rpilocator RSS Telegram Alert

Simple Python RSS feed tracker for rpiLocator

## Requirements

* Python 3.6

## Setup

### Python packages

A Python virtual environment doesn't have to be used, but is recommend.

```bash
python -m venv ./pilocatorEnv; \
source ./pilocatorEnv/bin/activate; \
pip install -r requirements.txt
```

### Telegram Credentials

This step isn't required if you don't want to send a Telegram message, run script without pass `-t` flag.

In the root dir of repo a *.env* file will need to be created.  If using Docker secrets, or passing in environmental variables with another method just make sure variables in *.env* match.

```text
BOT_TOKEN=
```

#### Telegram Bot Setup

Follow these instructions for obtaining a Telegram bot and the API Token.  Steps referenced are from [apprise Telegram Docs](https://github.com/caronc/apprise/wiki/Notify_telegram)

Telegram notifications require you to create a bot. It's only after this is done that you will gain a vital piece of information Apprise needs called the Token Identifier (or bot_token).

To do this you will have to open a communication (inside Telegram) to the BotFather. He is available to all users signed up to the platform. Once you've got a dialog box open to him:

1. Type: /newbot
2. Answer the questions it asks after doing this (which get the name of it, etc).
3. When you've completed step 2, you will be provided a bot_token that looks something like this: 123456789:alphanumeric_characters.
4. Type /start now in the same dialog box to enable and instantiate your brand new bot.

#### Warning

Don't share this Telegram Bot Token with anyone else, or push into a public location like accidentally onto Github

## Running

Script is run with the following optional parameters `python run.py [-h] [-a AGE] [-m MODEL] [-r REGION] [-t TRIAL]`, use `-h` flag for help and more information.

### Automating

Use Cron to have this script automatically run whenever you desire.  Though run aggressively and rpiLocator will block access to the site.  In their words, "If you are looking to create a notification system for **personal use**, please use the RSS feed and don't hit the site more than **once a minute**. High frequency bots will get blocked." I do 4 times a day, each 6 hours apart.

To access cron, use the command `crontab -l` to view your user cronjobs, and `crontab -e` to edit them.

```cron
0 */6 * * * /path/to/correct/python Path/To/Repository/run.py -a 0 -r US -m CM4 > /dev/null
```

#### Anacron

TODO: Include section on using Anacron, perfect alternative for a laptop or pc instead of cron for server.

#### Docker

TODO: Create Docker container for this, for kicks its kind of overkill

## Testing

### Linting

Python linting uses pylint and flake8.

A general pylint check will use following pylint command `pylint $(git ls-files '*.py');`

A general flake8 check will check for everything.  But for continuous integration the command used will be `flake8 . --count --show-source --statistics --exclude flaskEnv/`

```bash
flake8 --exclude flaskEnv/
```

Linting can also be done with Python Black, `black <file>`.

## References

* [rpilocator](https://rpilocator.com/)
* [Python reading RSS feed](https://www.tutorialspoint.com/python_text_processing/python_reading_rss_feed.htm)
* [Python send email gmail](https://mailtrap.io/blog/python-send-email-gmail/) - No longer used, but still good reference. Pull repo tag 1.0 for its use here.
* [apprise messaging library](https://pypi.org/project/apprise/)
