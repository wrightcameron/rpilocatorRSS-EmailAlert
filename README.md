# piLocator RSS Tracker

Simple Python RSS feed tracker for piLocator

## Requirements

* Python 3.6

## Setup

A Python virtual environment doesn't have to be used, but is recommend.  Otherwise jump to run after installing required pip packages.

```bash
python -m venv ./pilocatorEnv; \
source ./pilocatorEnv/bin/activate; \
pip install -r requirements.txt
```

## Running

Script is run with the following optional parameters `python run.py [-h] [-a AGE] [-m MODEL] [-r REGION] [-t TRIAL]`, use `-h` flag for help and more information.

### Automating

Use Cron to have this script automatically run whenever you desire.  Though run aggressively and piLocator will block access to the site.  In their words, "If you are looking to create a notification system for **personal use**, please use the RSS feed and don't hit the site more than **once a minute**. High frequency bots will get blocked." I do 4 times a day, each 6 hours apart.

To access cron, use the command `crontab -l` to view your user cronjobs, and `crontab -e` to edit them.

```cron
0 */6 * * *Path/To/Repository/run.py
```

## Testing

### Linting

Python linting uses pylint and flake8.

A general pylint check will use following pylint command `pylint $(git ls-files '*.py');`

A general flake8 check will check for everything.  But for continuous integration the command used will be `flake8 . --count --show-source --statistics --exclude flaskEnv/`

```bash
flake8 --exclude flaskEnv/
```

Linting can also be done with Python Black, `python black <file>`

## References

* [rpilocator](https://rpilocator.com/)
* [Python reading RSS feed](https://www.tutorialspoint.com/python_text_processing/python_reading_rss_feed.htm)
* [Python send email gmail](https://mailtrap.io/blog/python-send-email-gmail/)
