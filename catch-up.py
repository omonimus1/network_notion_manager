import os
import smtplib
from urllib.parse import urlparse
import datetime
import pytz
import requests
from notion_client import Client
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


# Set up Notion API client
notion = Client(auth= os.getenv("NOTION_API_KEY"))
# Set up SMTP client
smtp_server = os.getenv("SMTP_SERVER") 
smtp_port =  os.getenv("SMTP_PORT") 
smtp_username =  os.getenv("SMTP_USERNAME")
smtp_password =   os.getenv("SMTP_PASSWORD")
smtp_from_address =  os.getenv("SMTP_FROM_EMAIL")
sender_email =  os.getenv("SENDER_EMAIL")
notion_api_key = os.getenv("NOTION_API_KEY")
# Get current date and time in UTC timezone
utc_now = datetime.datetime.now(pytz.utc)

# Define function to send email using SMTP
def send_email(to_email, name_contacted_person):
    # Create a message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Networking and catch-up call"
    message["From"] = sender_email
    message["To"] = to_email
    text = f"Hi {name_contacted_person}, how are you doing? I haven't heard from you in a while, would you like to schedule a coffee break together? If so, reserve the time-slot here: https://www.cal.com/davidepollicino/networking"
    part1 = MIMEText(text, "plain")
    message.attach(part1)
    # Send the message
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password )
        result = server.sendmail(sender_email, to_email, message.as_string())
        if not result:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email to {result}")
    print("EMAIL SENT")


database_id = os.getenv("DATABASE_ID")
url = f"https://api.notion.com/v1/databases/{database_id}/query"
headers = {
    "Authorization": f"Bearer {notion_api_key}", 
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
data = {
    "filter": {
            "and": [
                {
                    "property": "last_contacted_date",
                    "date": {
                        "on_or_before": utc_now.strftime("%Y-%m-%d")
                    }
                }
            ]
        }
}

# Send the request to the Notion API
response = requests.post(url, headers=headers, json=data)
# Extract the response data
response_data = response.json()
print(response_data)
# Loop through the table rows and check if follow-up is needed
# Extract the properties of each row in the database
for row in response_data["results"]:
    email = row["properties"]["email"]["email"]
    full_name = row["properties"]["full_name"]["rich_text"][0]["text"]["content"]
    first_name = full_name.split()[0]
    last_contacted_date = row["properties"]["last_contacted_date"]["date"]["start"]
    
    # Print the properties for debugging
    print(f"Email: {email}, First Name: {first_name}, Last Contacted Date: {last_contacted_date}")
    print(email)
    # Calculate the difference between the current date and last contacted date
    # days_since_last_contacted = (utc_now - last_contacted_date).days
    
    # If the difference is greater than 40 days, send a follow-up email
    # if days_since_last_contacted > 5:
    send_email(sender_email, first_name)
     # Update the "last_contacted_date" property for the row
    notion.pages.update(
        page_id=row["id"],
        properties={
            "last_contacted_date": {
                "date": {
                    "start": utc_now.strftime("%Y-%m-%d")
                }
            }
        }
    )
