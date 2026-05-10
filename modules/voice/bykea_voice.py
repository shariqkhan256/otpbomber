from otpbomber.core import *
from otpbomber.localuseragent import *

async def bykea_voice(phone, client, out):
    name = 'bykea_voice'
    domain = 'bykea.com'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Content-Type': 'application/json'}
    phone_num = phone[-10:]
    try:
        response = await client.post('https://api.bykea.com/v1/user/otp/send', headers=headers, json={'country_code': '92', 'phone_number': phone_num, 'type': 'voice'})
        if response.status_code == 200:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})