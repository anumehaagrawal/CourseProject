import requests
from bs4 import BeautifulSoup
import pandas as pd
URL = "https://money.cnn.com/data/hotstocks/index.html"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(class_="wsod_dataTable wsod_dataTableBigAlt")
df = pd.read_html(str(results))[0]
print(df)
df.to_csv('/Users/devangag/UIUC/CS410/Project/stocks.csv', index= False, header= True)
