import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ChaparinoHub:
    def __init__(self):
        self.bale_key = os.getenv("BALE_ACCESS_KEY")
        self.bale_bot = os.getenv("BALE_BOT_ID")
        self.sms_key = os.getenv("SMS_IR_KEY")
        self.sms_line = os.getenv("SMS_IR_LINE")

    @staticmethod
    def normalize_phone(phone: str, to_international: bool = False):
        clean_phone = "".join(filter(str.isdigit, str(phone)))
        if len(clean_phone) == 10 and clean_phone.startswith("9"):
            clean_phone = "0" + clean_phone
        if clean_phone.startswith("09"):
            return "98" + clean_phone[1:] if to_international else clean_phone
        if clean_phone.startswith("989"):
            return clean_phone if to_international else "0" + clean_phone[2:]
        return clean_phone

    def send_bale(self, phone: str, text: str):
        formatted_phone = self.normalize_phone(phone, to_international=True)
        url = "https://safir.bale.ai/api/v3/send_message"
        payload = {
            "bot_id": int(self.bale_bot),
            "phone_number": formatted_phone,
            "message_data": {"message": {"text": text}}
        }
        headers = {"api-access-key": self.bale_key}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.json()

    def send_sms(self, phone: str, text: str):
        formatted_phone = self.normalize_phone(phone, to_international=False)
        url = "https://api.sms.ir/v1/send/bulk"
        payload = {
            "lineNumber": int(self.sms_line),
            "messageText": f"{text}\nلغو ۱۱",
            "mobiles": [formatted_phone]
        }
        headers = {"X-API-KEY": self.sms_key}
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.json()