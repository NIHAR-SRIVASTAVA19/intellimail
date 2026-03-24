import email
import imaplib
import os
from email.header import decode_header

from langchain_core.tools import tool

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

@tool
def get_inbox(limit: int) -> list[dict]:
    """
    Retrieve the most recent emails from the inbox.

    Use this tool when the user requests to read, check, or fetch emails from their inbox.

    Parameters:
        limit (int): The number of most recent emails to retrieve.

    Returns:
        list[dict]: A list of email summaries, each containing:
            - id: The email's unique identifier.
            - from: The sender's email address and name.
            - subject: The subject line of the email.
    """
    print(f"Fetching most recent emails from inbox...  limit:{limit}")
    results = []

    # connect to Gmail IMAP
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # login
    imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # open inbox
    imap.select("INBOX")

    # search all emails
    status, messages = imap.search(None, "ALL")

    mail_ids = messages[0].split()

    latest_emails = mail_ids[-limit:]
    latest_emails = list(reversed(latest_emails))

    for mail_id in latest_emails:
        status, msg_data = imap.fetch(mail_id, "(RFC822)")

        for response in msg_data:
            if isinstance(response, tuple):

                msg = email.message_from_bytes(response[1])

                # SUBJECT
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")

                # SENDER
                sender = msg.get("From")

                results.append({
                    "id": mail_id.decode(),  # ← decode bytes to str
                    "from": sender,
                    "subject": subject,
                })

    imap.logout()

    return results



def extract_body(msg):
    """
    Returns:
    - plain text if available
    - otherwise RAW HTML
    """

    text_body = ""
    html_body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # ignore attachments
            if "attachment" in content_disposition:
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            if content_type == "text/plain":
                text_body = payload.decode(errors="ignore")

            elif content_type == "text/html":
                html_body = payload.decode(errors="ignore")

    else:
        payload = msg.get_payload(decode=True)
        if payload:
            text_body = payload.decode(errors="ignore")

    # prefer plain text
    if text_body:
        return text_body.strip()

    # fallback → RAW HTML (no parsing)
    if html_body:
        return html_body.strip()

    return ""



@tool
def get_mail_body(mail_id: str) -> dict:  # ← str, not int
    """
    Retrieve the full body of a specific email by its ID.

    Use this tool when the user wants to read the content/body of a specific email.
    Always call get_inbox first to obtain the email ID before using this tool.

    Parameters:
        mail_id (str): The unique identifier of the email to retrieve.

    Returns:
        dict: A dictionary containing the full email details:
            - id: The email's unique identifier.
            - from: The sender's name and email address.
            - subject: The subject line of the email.
            - body: The full text content of the email (capped at 3000 characters).
    """
    print(f"Fetching mail details from inbox...  mail_id:{mail_id}")
    result = {}

    # connect to Gmail IMAP
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # login
    imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    # open inbox
    imap.select("INBOX")

    # ← encode str back to bytes for IMAP fetch
    status, msg_data = imap.fetch(mail_id.encode(), "(RFC822)")

    for response in msg_data:
        if isinstance(response, tuple):

            msg = email.message_from_bytes(response[1])

            # SUBJECT
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            # SENDER
            sender = msg.get("From")

            # BODY
            body = extract_body(msg)

            result = {
                "id": mail_id,
                "from": sender,
                "subject": subject,
                "body": body[:3000]  # safe limit
            }

    imap.logout()
    print(result)
    return result