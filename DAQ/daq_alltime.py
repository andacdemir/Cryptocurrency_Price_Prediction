import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from datetime import datetime


# Extract data from the HTML table on coinmarketcap.com
# given the id of the cryptocurrency:

#yearmonthday like 20180214
now = datetime.now()
start_date = '20120101'
end_date = str(now.year + now.month + now.day)
coin_id = 'bitcoin'
url = 'https://coinmarketcap.com/currencies/' + coin_id + '/historical-data/' \
      + '?start=' + start_date +'&end=' + end_date


res = requests.get(url)
soup = BeautifulSoup(res.content,"lxml")
table = soup.find('table')
df = pd.read_html(str(table))
# pretty print df
print(tabulate(df[0], headers='keys', tablefmt='psql'))


# timestamps and stores the csv file
location = 'allTime_' + coin_id + str(now.year) + str(now.month) \
           + str(now.day) + '.csv'
df[0].to_csv(location)

