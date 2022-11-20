import requests


def sendSMS(contactno, message):
    try:
        url = "https://www.fast2sms.com/dev/bulk"
        payload = "sender_id=FSTSMS&message="+message + \
            "&language=english&route=p&numbers="+contactno
        headers = {
            'authorization': "eKzdX84VADNTguh7l23HkxMQJaqYrEZtSwv01IsUm9obRyPOWCO3B1Cc2xo6sSQJtDehRG4IpYFmviUq",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        s1 = response.text
        return s1
    except ConnectionError:
        msg = "Please connect with Internet"
        return msg
