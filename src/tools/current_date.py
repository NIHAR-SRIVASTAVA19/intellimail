from datetime import datetime
from zoneinfo import ZoneInfo

from langchain_core.tools import tool


@tool
def current_datetime() -> dict:
    """
    Returns the current date and time in Indian Standard Time (IST).

    Use this tool when:
    - The user asks for today's date
    - The user refers to relative dates (today, tomorrow, next week)
    - Time or scheduling context is required

    Returns:
        dict: Structured current datetime information.
    """

    now = datetime.now(ZoneInfo("Asia/Kolkata"))

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
        "timezone": "IST",
        "iso_datetime": now.isoformat()
    }