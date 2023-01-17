import argparse
import feedparser
import datetime
import smtplib
from email.mime.text import MIMEText
from dateutil import parser

import os
from dotenv import load_dotenv

load_dotenv()




def isDateOld(dateStr: str, dateRange: int) -> bool:
    # Mon, 16 Jan 2023 11:54:13 GMT
    date = parser.parse(dateStr)
    now = datetime.datetime.now(datetime.timezone.utc)
    dateDelta = now - date
    return dateDelta.days > dateRange

def sendEmail(subject, body):
    load_dotenv()
    emailSender = os.getenv('emailSender')
    emailSenderServer = os.getenv('emailSenderServer')
    emailSenderPassword = os.getenv('emailSenderPassword')
    emailReciever = os.getenv('emailReciever')
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = emailSender
    msg['To'] = emailReciever
    smtp_server = smtplib.SMTP_SSL(emailSenderServer, 465)
    smtp_server.login(emailSender, emailSenderPassword)
    smtp_server.sendmail(emailSender, emailReciever, msg.as_string())
    smtp_server.quit()

def sendEmail():
    pass

def run(region: str, catagory: str, dateRange: int, isTrial: bool = False) -> None:
    # Get piLocatorFeed
    #TODO What if we want to view all regions or all catagories now?
    piLocatorFeed = feedparser.parse(f"https://rpilocator.com/feed/?country={region}&cat={catagory}")

    for entry in piLocatorFeed.entries:
        # TODO Maybe move these satements to a log
        # Determine if the pi is model, region, and date match
        if isDateOld(entry.published, dateRange):
            # RSS Feed is ordered by date, so if date is old enough break loop
            break
        print(entry.published)
        print("******")
        print(entry.summary)
        print("------News Link--------")
        print(entry.link)
        # If pi is in stock send email notification
        subject = "Email Subject"
        body = "This is the body of the text message"
        if not isTrial:
            sendEmail(subject, body)
        else:
            print("Trial run, not sending email.")
        # TODO What if we have more than one entry, we still want one email
        # TODO Have way to prevent duplicate email from being sent, most likely temp file.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PiLocatorRSSAlert: RSS Feed Reader Alert Script. Send email when desirable Pi found."
    )
    # TODO Default should be all regions and all catagories instead of US and CM4.  It's just easier for me right now
    parser.add_argument("-a", "--age", type=int, help="The amount of day's old an alert can be.", default=0)
    parser.add_argument("-m", "--model", type=str, help="Pi Model to alert for.", default='US')
    parser.add_argument("-r", "--region", type=str, help="Region the Pi is sold from.", default='CM4')
    parser.add_argument("-t", "--trial", type=bool, help="Run script without pushing any potential emails", default=False)
    args = parser.parse_args()

    run(args.region, args.model, args.age, args.trial)
