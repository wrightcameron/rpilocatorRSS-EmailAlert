import argparse
import feedparser
import re
import datetime


def isDateOld(dateStr: str) -> bool:
    # Mon, 16 Jan 2023 11:54:13 GMT
    from dateutil import parser
    date = parser.parse(dateStr)
    now = datetime.datetime.now(datetime.timezone.utc)
    dateDelta = now - date
    return dateDelta.days > AGE

# TODO Model and Region functions are same, combine them.
def checkRegion(region: str) -> bool:
    if REGION is None:
        return True
    p = re.search(f'({REGION})', region)
    return p is None

def checkModel(model: str) -> bool:
    if MODEL is None:
        return True
    p = re.search(f'({MODEL})', model)
    return p is None

def checkConditions():
    pass

def sendEmail():
    pass

def run() -> None:
    # Get piLocatorFeed
    piLocatorFeed = feedparser.parse("https://rpilocator.com/feed/")

    for entry in piLocatorFeed.entries:
        # TODO Maybe move these satements to a log
        # Determine if the pi is model, region, and date match
        if isDateOld(entry.published):
            # RSS Feed is ordered by date, so if date is old enough break loop
            break
        if checkRegion(entry.title) or checkModel(entry.title):
            continue
        print(entry.published)
        print("******")
        print(entry.summary)
        print("------News Link--------")
        print(entry.link)
        # If pi is in stock send email notification
        # TODO What if we have more than one entry, we still want one email
        # TODO Have way to prevent duplicate email from being sent, most likely temp file.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PiLocatorRSSAlert: RSS Feed Reader Alert Script. Send email when desirable Pi found."
    )
    parser.add_argument("-a", "--age", type=int, help="The amount of day's old an alert can be.")
    parser.add_argument("-m", "--model", type=str, help="Pi Model to alert for.")
    parser.add_argument("-r", "--region", type=str, help="Region the Pi is sold from.")
    args = parser.parse_args()

    global AGE 
    global MODEL
    global REGION

    AGE = args.age
    MODEL = args.model
    REGION = args.region
    run()
