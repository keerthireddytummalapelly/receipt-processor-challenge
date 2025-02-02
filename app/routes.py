from fastapi import APIRouter, HTTPException
from app.models import Receipt, ReceiptId, Points
from app.database import receipt_map, generate_receipt_id, parse_date, parse_time
import math
from datetime import datetime

router = APIRouter()

@router.post("/receipts/process", response_model=ReceiptId)
async def process_receipt(receipt: Receipt):
    """
    Submits a receipt for processing.
    
    **Parameters:**
    - **retailer** (str): The name of the retailer or store the receipt is from.
    - **purchaseDate** (str): The date of the purchase printed on the receipt.
    - **purchaseTime** (str): The time of the purchase printed on the receipt (`HH:MM` 24-hour format).
    - **items** (List[Item]): List of purchased items.
    - **total** (str):  The total amount paid on the receipt (`X.XX`) format.
    
    **Returns:**
    - **receiptId** (str): Returns the ID assigned to the receipt.
    """

    # Validate the input feilds
    if len(receipt.items) == 0:
        raise HTTPException(status_code=400, detail="The receipt is invalid.") 
    
    # Parse purchase date on the receipt
    receipt.purchaseDate = parse_date(receipt.purchaseDate)

    # Parse purchase time on the receipt
    receipt.purchaseTime = parse_time(receipt.purchaseTime)
    
    if receipt.purchaseDate is None or receipt.purchaseTime is None:
        raise HTTPException(status_code=400, detail="The receipt is invalid.") 
    
    
    # Generate the receipt id
    receipt_id = generate_receipt_id(receipt)

    # Avoids recomputaion if id is already present in the dictionary
    if receipt_id in receipt_map:
        return {"id": receipt_id}

    # Initialize points
    points = 0

    # One point for every alphanumeric character in retailer name
    points += sum(c.isalnum() for c in receipt.retailer)
    
    # 50 points if the total is a round dollar amount with no cents.
    if receipt.total.endswith(".00"):
        points += 50

    # 25 points if the total is a multiple of 0.25.
    if float(receipt.total) % 0.25 == 0:
        points += 25

    # 5 points for every two items on the receipt.
    points += (len(receipt.items) // 2) * 5

    # 6 points if the day in the purchase date is odd.
    if receipt.purchaseDate.day % 2 != 0:
        points += 6

    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up. The result is the number of points earned.
    for item in receipt.items:
        item.shortDescription = item.shortDescription.strip()
        if len(item.shortDescription) % 3 == 0:
            points += math.ceil(float(item.price) * 0.2)

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    lower_bound = datetime.strptime("14:00:00.000", "%H:%M:%S.%f").time()
    upper_bound = datetime.strptime("16:00:00.000", "%H:%M:%S.%f").time()
    if lower_bound < receipt.purchaseTime < upper_bound:
        points += 10
    
    # Store points calculated in dict to avoid recomputing
    receipt_map[receipt_id] = points

    return {"id": receipt_id}


@router.get("/receipts/{id}/points", response_model=Points)
async def get_points(id: str):
    """
    Get the points awarded for a given receipt.

    **Parameters:**
    - **id** (str): The unique identifier of the receipt.

    **Returns:**
    - **points** (int): Returns the number of points awarded.

    """
    # Check for id in the receipt_map dictionary
    if id not in receipt_map:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    
    return {"points": receipt_map[id]}



    
    
