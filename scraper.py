import requests
from bs4 import BeautifulSoup
import pandas as pd
URL_TWO = "https://money.cnn.com/quote/quote.html?symb=PFE"
URL = "https://money.cnn.com/data/hotstocks/index.html"
page = requests.get(URL)
page_two = requests.get(URL_TWO)
soup = BeautifulSoup(page.content, "html.parser")
soup_two = BeautifulSoup(page_two.content, "html.parser")
results = soup.find(class_="wsod_dataTable wsod_dataTableBigAlt")
results_two = soup_two.find(class_="wsod_quoteData")
df = pd.read_html(str(results))[0]
df_two = pd.read_html(str(results_two))[0]
#print(df)
print(df_two)
df.to_csv('/Users/devangag/UIUC/CS410/Project/stocks.csv', index= False, header= True)