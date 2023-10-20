import requests
from django.conf import settings


def send_otp(mobile,otp):
    url = f"{settings.INFOBIP_BASE_URL}/sms/1/text/single"
    headers = {"content-type":"application/x-www-form-urlencoded"}
    payload = {
        "from": "Bd Travel Platform",
        "to": mobile,
        "text": f"Your OTP is: {otp}",
    }
    response = requests.get(url, json=payload, headers=headers)
    return bool(response.ok)
