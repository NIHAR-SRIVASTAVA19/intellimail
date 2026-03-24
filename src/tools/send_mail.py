import os
import smtplib
from email.message import EmailMessage

from langchain_core.tools import tool
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

@tool
def send_mail(email: str, subject: str, body: str) -> str:
    """
    Send an email to a recipient.

    Use this tool when the user requests to send an email or compose and send a message.

    Parameters:
        email (str): Recipient's email address.
        subject (str): Subject line of the email.
        body (str): Main content/message of the email.

    Returns:
        str: Confirmation message indicating whether the email was sent successfully.
    """


    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("✅ Email sent successfully")
    return f"Mail sent successfully to {email}"