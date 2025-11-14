import requests

def send_sms(api_key, message, recipient):
    url = "https://api.sms.net.bd/sendsms"

    payload = {
        "api_key": api_key,
        "msg": message,
        "to": recipient
    }

    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        return {"error": True, "msg": str(e)}
