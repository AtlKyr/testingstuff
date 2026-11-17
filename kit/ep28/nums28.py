import json
from decimal import Decimal, ROUND_HALF_UP
R=json.load(open('results28.json'))
hu=lambda x,q='1': int(Decimal(str(x)).quantize(Decimal(q),rounding=ROUND_HALF_UP))
assert hu(R['cluster10']*100)==65
assert R['worst10_out']==10 and R['best10_out']==10
assert round(R['max_lead'],-3)==5000 and R['max_lead']>5000
assert round(R['bh'],-3)==70000 and round(R['final'],-3)==40000 and round(R['bh']-R['final'],-3)==30000
assert R['lead_flip']=='2020-03-23' and R['max_lead_date']=='2009-03-09'
print('numbers OK')
