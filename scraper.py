import requests
from bs4 import BeautifulSoup
import pandas as pd
URL = "https://money.cnn.com/data/hotstocks/index.html"
URL_two = "https://money.cnn.com/quote/quote.html?symb=PFE" #the symbol can be changed to whatever stock symbol
page = requests.get(URL)
page_two = requests.get(URL_two)
soup = BeautifulSoup(page.content, "html.parser")
soup_two = BeautifulSoup(page_two.content, "html.parser")
results = soup.find(class_="wsod_dataTable wsod_dataTableBigAlt")
results_two = soup_two.find("h1",class_="wsod_fLeft")
results_three = soup_two.find("td",class_="wsod_last")
results_four = soup_two.find("span",class_="posData")
df = pd.read_html(str(results))[0]
data = [[results_two.text,results_three.text[0:5], results_four.text]]
df_two = pd.DataFrame(data, columns = ['Stock Name', 'Stock Price', '% Change'])
print(df)
print(df_two)
df.to_csv('/Users/devangag/UIUC/CS410/Project/stock_list.csv', index= False, header= True)
df_two.to_csv('/Users/devangag/UIUC/CS410/Project/stock_sample.csv', index= False, header= True)
