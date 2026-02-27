import re
import pandas as pd
from utils.schema import validate_schema

def parse_sms_transaction(sms_text: str):

    #Extract amount
    amount_match = re.search(r'Rs\.?\s?([\d,]+\.?\d*)', sms_text)
    amount = float(amount_match.group(1).replace(",", "")) if amount_match else None

    #Debited or credicted
    if "debit" in sms_text.lower():
        txn_type = "debit"
    elif "credit" in sms_text.lower():
        txn_type = "credit"
    else:
        txn_type = None

    #Extracting date
    date_match = re.search(r'(\d{2}-\d{2}-\d{4})', sms_text)
    date = pd.to_datetime(date_match.group(1), format = "%d-%m-%Y") if date_match else None

    #Balance
    balance_match = re.search(r'Bal[:\s]*Rs\.?\s?([\d,]+\.?\d*)', sms_text, re.IGNORECASE)
    if balance_match and balance_match.group(1):
        balance = float(balance_match.group(1).replace(",",""))
    else:
        balance = None

    #merchant(basic rule: search for word after 'at')
    merchant_match = re.search(r'at\s([A-Za-z0-9\s]+)', sms_text)
    merchant = merchant_match.group(1).strip() if merchant_match else None

    data = {
        "date": date,
        "amount": amount,
        "type": txn_type,
        "merchant": merchant,
        "category": None,
        "balance": balance,
        "source": "sms"
    }

    df = pd.DataFrame([data])

    return validate_schema(df)