import argparse
import datetime
import feedparser
import os
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText
from os.path import exists


def isDateOld(dateStr: str, dateRange: int) -> bool:
    """Compare the date of the listing to the date Range specified by user

    Args:
        dateStr (str): GMT date from RSS entry
        dateRange (int): date range user specified when running script

    Returns:
        bool: _description_
    """
    date = datetime.strptime(dateStr, "%a, %d %b %Y %H:%M:%S %Z")
    now = datetime.now()
    dateDelta = now - date
    return dateDelta.days > dateRange


def updateDateRange(lastCheckDate: datetime, dateRange: str) -> None:
    """Update date Range if passed in datetime is less days from now till then.

    Args:
        lastCheckDate (datetime): datetime object found from persistent file
        dateRange (str): date range user specified when running script

    Returns:
        _type_: _description_
    """
    if lastCheckDate is None:
        return dateRange
    now = datetime.now()
    dateDelta = now - lastCheckDate
    if dateDelta.days < dateRange:
        return dateDelta.days
    else:
        return dateRange


def sendEmail(subject: str, body: str) -> None:
    """Send email with information based on environmental variables passed in.

    Args:
        subject (str): Email subject
        body (str): Email body
    """
    # TODO What if .env file is empty?
    load_dotenv()
    sender = os.getenv("EMAIL_SENDER")
    SenderSMTP = os.getenv("SENDER_SMTP")
    senderPassword = os.getenv("SENDER_PASSWORD")
    reciever = os.getenv("EMAIL_RECEIVER")

    if senderPassword:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = reciever
        try:
            smtp_server = smtplib.SMTP_SSL(SenderSMTP, 465)
            smtp_server.login(sender, senderPassword)
            smtp_server.sendmail(sender, reciever, msg.as_string())
            smtp_server.quit()
        except Exception:
            print("Error: Failure to send email")
        else:
            print("Email Sent Successfully!")
    else:
        print(
            "Warning: No email account name or password found from env, not sending email."
        )


def createPersistantFile(date: datetime) -> None:
    """create persistent file in /tmp/ directory so next time
       script runs it knows listings it already emailed/mentioned.

    Args:
        date (datetime): datetime object, should be current time.
    """
    op = datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
    fname = "/tmp/rpiLocator.tmp"
    with open(fname, "w") as f:
        f.write(op)


def readPersistantFile() -> datetime:
    """Read persistent file

    Returns:
        datetime: datetime object found in persistent file converted from string.
    """
    fname = "/tmp/rpiLocator.tmp"
    if not exists(fname):
        return None
    try:
        with open(fname, "r") as f:
            date = f.read()
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    except Exception:
        print(
            "Error: Issues reading persisant file, probably was modfied to not be a date."
        )
    else:
        date = None
    return date


def run(region: str, category: str, dateRange: int, isTrial: bool = False) -> None:
    """Main function

    Args:
        region (str): Region to check for rPi
        category (str): Model of rPi
        dateRange (int): How far back in time to check postings
        isTrial (bool, optional): Send email if False, otherwise
            only print to stout. Defaults to False.
    """
    # Get piLocatorFeed
    print(
        f"Checking rpilocator for {category if category else 'all' } Pi Models in {region if region else 'all'} region(s) in the last {dateRange} days."
    )
    # Add url paramters based on if region and category were passed in.
    url = "https://rpilocator.com/feed/"
    if region and category:
        url = f"{url}?country={region}&cat={category}"

    elif region:
        url = f"{url}?country={region}"
    elif category:
        url = f"{url}?cat={category}"
    piLocatorFeed = feedparser.parse(url)
    piFound = False
    # dateRange = updateDateRange(readPersistantFile(), dateRange)
    body = f"{region} Store carrying {category} pi's posted stock. Here are listings."
    # Collect all entries that meet condition to push in one email.
    for entry in piLocatorFeed.entries:
        # Determine if the pi is model, region, and date match
        if isDateOld(entry.published, dateRange):
            # RSS Feed is ordered by date, so if date is old enough break loop
            break
        piFound = True
        # TODO Have way to prevent duplicate email from being sent, most likely temp file.
        body += f"\n{entry.summary}\n{entry.published}\n{entry.link}\n------------------------"
        # If pi is in stock send email notification

    # Iterate through entries to build one email
    if piFound:
        subject = f"rpilocator: {category} models in region {region} posted!"
        if not isTrial:
            sendEmail(subject, body)
        else:
            print("Trial run, not sending email.")
        # DateRange of 0 would still have that last 24 hours postings show up
        # TODO Need to compare listings by hour or minute for persitant file to work properly.
        # if dateRange == 0:
        #     createPersistantFile(datetime.now())
        print(subject)
        print(body)
        print("******")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PiLocatorRSSAlert: RSS Feed Reader Alert Script. Send email when desirable Pi found."
    )
    parser.add_argument("-a", "--age", type=int, help="The amount of day's old an alert can be.", default=0)
    parser.add_argument("-m", "--model", type=str, help="Pi Model to alert for.")
    parser.add_argument("-r", "--region", type=str, help="Region the Pi is sold from.")
    parser.add_argument("-t", "--trial", action='store_true', help="Run script without pushing any potential emails")
    args = parser.parse_args()
    # TODO What if someone wanted to check multiple regions or models.  Url allows multiple parameters
    run(args.region, args.model, args.age, args.trial)
