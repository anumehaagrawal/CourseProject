import requests
from bs4 import BeautifulSoup
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


#URL_two = "https://money.cnn.com/quote/quote.html?symb=PFE" #the symbol can be changed to whatever stock symbol

#df.to_csv('/Users/devangag/UIUC/CS410/Project/stock_list.csv', index= False, header= True)
#df_two.to_csv('/Users/devangag/UIUC/CS410/Project/stock_sample.csv', index= False, header= True)

def TopStocks():
    URL = "https://money.cnn.com/data/hotstocks/index.html"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="wsod_dataTable wsod_dataTableBigAlt")
    df = pd.read_html(str(results))[0]
   
    return df

def SpecificStock(stockURL):
    page_two = requests.get(stockURL)

    soup_two = BeautifulSoup(page_two.content, "html.parser")

    results_two = soup_two.find("h1",class_="wsod_fLeft")
    results_three = soup_two.find("td",class_="wsod_last")
    results_four = soup_two.find("span",class_="posData")

    data = [[results_two.text,results_three.text[0:5], results_four.text]]
    df_two = pd.DataFrame(data, columns = ['Stock Name', 'Stock Price', '% Change'])
    return df_two

def LinksForSentimentAnalysis(stockURL):
   page_three = requests.get(stockURL)
   soup_three = BeautifulSoup(page_two.content, "html.parser")
   results_five = soup_two.find_all("td", class_="firstCol")
   df_three = pd.DataFrame(columns = ['URLs'])
   for result in results_five:
    links = result.find_all("a")
    for link in links:
        data_two = link.text.strip()
        df_three = df_three.append({'URLs': data_two}, ignore_index=True)
     
    return df_three
