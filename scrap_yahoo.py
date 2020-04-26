import requests
import pandas as pd

wikiurl = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
wikiresponse = requests.get(wikiurl)

data = {'Company':[]}

wikifirst = wikiresponse.text.split('0001555280')[0]
wikitable = wikifirst.split('component stocks')[3]
hyperlink = wikitable.split('href=')
for position in range(len(hyperlink)):
        if 'nyse'  in hyperlink[position]:
            data['Company'].append(hyperlink[position].split('">')[1].split('</')[0])
        elif  'nasdaq' in hyperlink[position]:
            data['Company'].append(hyperlink[position].split('">')[1].split('</')[0])


indicators = {'Previous close':[],
'Open':[],
'Bid':[],
'Ask':[],
"Day's range":[],
'52 Week Range':[],
'Volume':[],
'Avg. volum':[],
'Market cap':[],
'Beta (5Y monthly)':[],
'PE ratio (TTM)':[],
'EPS (TTM)':[],
'Earnings date':[],
'Forward dividend &amp; yield':[],
'Ex-dividend date':[],
'1y target est':[]}

counter = 0

for company in data['Company']:
    url = ('https://in.finance.yahoo.com/quote/'+
             company +'?p='+ company)
    response = requests.get(url)
    html_text = response.text
    for indicator in indicators:
        try:
            if indicator == 'Day\'s range':
                splitlist = html_text.split('Day&#x27;s range')
                dataValue = splitlist[1].split('">')[1].split('</td')[0]
                indicators[indicator].append(dataValue)
            else:
                splitlist = html_text.split(indicator)
                dataValue = splitlist[1].split('">')[2].split('</span>')[0]
                indicators[indicator].append(dataValue)
        except:
            indicators[indicator].append('N/A')


data.update(indicators)


df = pd.DataFrame(data)

print(df.head())