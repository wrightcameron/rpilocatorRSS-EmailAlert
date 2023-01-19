import argparse
import datetime
import feedparser
import os
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText

def isDateOld(dateStr: str, dateRange: int) -> bool:
    """_summary_

    Args:
        dateStr (str): _description_
        dateRange (int): _description_

    Returns:
        bool: _description_
    """
    date = datetime.strptime(dateStr,'%a, %d %b %Y %H:%M:%S %Z')
    now = datetime.now()
    dateDelta = now - date
    return dateDelta.days > dateRange

def sendEmail(subject: str, body: str) -> None:
    """_summary_

    Args:
        subject (str): _description_
        body (str): _description_
    """
    load_dotenv()
    sender = os.getenv('EMAIL_SENDER')
    SenderSMTP = os.getenv('SENDER_SMTP')
    senderPassword = os.getenv('SENDER_PASSWORD')
    reciever = os.getenv('EMAIL_RECEIVER')
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = reciever
    smtp_server = smtplib.SMTP_SSL(SenderSMTP, 465)
    smtp_server.login(sender, senderPassword)
    smtp_server.sendmail(sender, reciever, msg.as_string())
    smtp_server.quit()

def run(region: str, catagory: str, dateRange: int, isTrial: bool = False) -> None:
    """

    Args:
        region (str): _description_
        catagory (str): _description_
        dateRange (int): _description_
        isTrial (bool, optional): _description_. Defaults to False.
    """
    # Get piLocatorFeed
    print(f"Checking rpilocator for {catagory if catagory else 'all' } Pi Models in {region if region else 'all'} region(s) in the last {dateRange} days.")
    # Add url paramters based on if region and catagory were passed in.
    url = "https://rpilocator.com/feed/"
    if region and catagory:
        url = f"{url}?country={region}&cat={catagory}"
        
    elif region:
        url = f"{url}?country={region}"
    elif catagory:
        url = f"{url}?cat={catagory}"
    # url = './1k1avZm_'  # FOR DEBUGGING
    piLocatorFeed = feedparser.parse(url)
    piFound = False
    body = f"{region} Store carrying {catagory} pi's posted stock. Here are listings." 
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
        subject = f"rpilocator: {catagory} models in region {region} posted!"
        if not isTrial:
            sendEmail(subject, body)
        else:
            print("Trial run, not sending email.")
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

    run(args.region, args.model, args.age, args.trial)
