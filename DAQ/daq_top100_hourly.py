from coinmarketcap import Market
import pandas as pd
import time
from tabulate import tabulate

market = Market()
coins = market.ticker()
# this creates a dataframe with the top 100 coins
df = pd.DataFrame([pd.Series(coins[i]) for i in range(100)]).set_index('id')
# Drop these columns from the data frame:
df.drop(['cached', 'name', 'rank', 'symbol'], axis=1, inplace=True)
# pretty print df
print(tabulate(df, headers='keys', tablefmt='psql'))


# timestamps and stores the csv file, For Windows, the epoch is January 1, 1601
location = 'top100_hrly@' + str(time.time())+'.csv'
df.to_csv(location)
# waits an hour until collecting data again
time.sleep(3600)