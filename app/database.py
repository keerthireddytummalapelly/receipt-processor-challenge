from typing import Dict, Optional
from app.models import Receipt
import uuid
import hashlib
from datetime import datetime

# In-memory database
receipt_map: Dict[str, int] = {}

def generate_receipt_id(receipt: Receipt) -> str:
    
    """
    Generates a unique and consistent ID for a receipt using key attributes, ensuring that identical receipt details always produce the same ID.

    Parameters:
    - receipt (Receipt): Receipt object

    Returns:
    - str: An ID to uniquely identify the receipt.

    """
    # Convert item list to a hashed string
    sorted_items = sorted(receipt.items, key=lambda item: item.shortDescription)
    item_hashes = [hashlib.sha1(f"{item.shortDescription}:{item.price}".encode()).hexdigest() for item in sorted_items]
    items_hash = hashlib.sha1("".join(item_hashes).encode()).hexdigest()

    # Create a unique string combining all receipt details
    receipt_string = f"{receipt.retailer}.{receipt.purchaseDate}.{receipt.purchaseTime}.{items_hash}.{receipt.total}"
    
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, receipt_string))



def parse_date(date_str: str) -> Optional[datetime.date]:

    """
    Attempts to parse the input date string using multiple date formats.

    Parameters:
    - date_str (str): Date as a string, which may be in different formats.

    Returns:
    - Optional[datetime.date]: Parsed date in YYYY-MM-DD format if successfully parsed, otherwise None.
    """

    # Valid date formats
    date_formats = [
            "%Y-%m-%d",  # Ex: 2024-02-01
            "%m/%d/%Y",  # Ex: 02/01/2024
            "%d/%m/%Y",  # Ex: 01/02/2024
            "%m-%d-%Y",  # Ex: 02-01-2024
            "%d-%m-%Y",  # Ex: 01-02-2024
            "%B %d, %Y",  # Ex: February 1, 2024
            "%b %d, %Y",  # Ex: Feb 1, 2024
            "%B %d %Y",  # Ex: February 1 2024
            "%b %d %Y",  # Ex: Feb 1 2024
        ]
    
    for format in date_formats:
        try:
            # Parse time into a datetime.date object
            parsed_date = datetime.strptime(date_str, format).date()
            return parsed_date 
        except ValueError:
            continue 
    return None

def parse_time(time_str: str) -> Optional[datetime.time]:
    
    """
    Attempts to parse the input time string using multiple 24-hour formats.

    Parameters:
    - time_str (str): Time as a string, which may be in different formats.

    Returns:
    - Optional[datetime.time]: `time` object if the format is valid, otherwise None.

    """

    # Valid 24-Hr time formats
    time_formats = [
        "%H:%M",          # Ex: 14:30
        "%H:%M:%S",       # Ex: 14:30:15
        "%H:%M:%S.%f",    # Ex:  14:30:15.123
        "%H%M",           # Ex: 1430
    ]
    
    for format in time_formats:
        try:
            # Parse time into a datetime.time object
            time_obj = datetime.strptime(time_str, format).time()
            return time_obj
        except ValueError:
            continue  
    return None
  

