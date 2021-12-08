from flask import Flask, json, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, Request
from prettytable import PrettyTable

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

@app.route('/_top_stocks/', methods=['GET'])
def TopStocks():
    URL = "https://money.cnn.com/data/hotstocks/index.html"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="wsod_dataTable wsod_dataTableBigAlt")
    df = pd.read_html(str(results))[0]

    #sort the pandas data frame by the greatest change
    def change_percent_and_sort(df, col_name):
        df[col_name] = df[col_name].str.replace(r'%', '')
        df[col_name] = df[col_name].astype(float)
        return df.sort_values([col_name], ascending = False)

    df_sorted = change_percent_and_sort(df, '%\xa0Change')
    df_sorted = df_sorted.rename(columns={'%\xa0Change': 'PercentChange'})
    x = PrettyTable()
    x.field_names = ["Company", "Price", "PercentChange"]
    for row in df.itertuples(index=True, name='Pandas'):
        print(row.count)
        x.add_row([row.Company, row.Price, row.Change])
    print(x)
    return x.get_html_string()


@app.route('/_top_stocks_news/', methods=['GET'])
def TopNewsInfo():
    url = 'https://money.cnn.com/data/markets/'
    req = Request(url)
    response = urlopen(req)
    html = BeautifulSoup(response)
    html = html.find(class_="column right-column")
    html = html.find(class_="module")
    link_html = html.find_all(class_="summary-hed")

    links = []
    for link_info in link_html:
        links.append(link_info['href'])
        #print(link_html[0]['href'])

    html = html.find_all(class_="thumb-caption")

    headlines = []
    for headline in html:
        headlines.append(headline.text.strip())

    x = PrettyTable()
    x.field_names = ["Headlines", "Links"]
    for index in range(min(len(links), len(headlines))):
        x.add_row([headlines[index], links[index]])

    print(x)
    return x.get_html_string()
    # return jsonify(df.to_string())

@app.route('/stock', methods=['GET'])
def SpecificStock():
    stockURL = request.args.get('url')
    page_two = requests.get(stockURL)

    soup_two = BeautifulSoup(page_two.content, "html.parser")

    results_two = soup_two.find("h1",class_="wsod_fLeft")
    results_three = soup_two.find("td",class_="wsod_last")
    results_four = soup_two.find("span",class_="posData")
    print(stockURL)
    data = [results_two.text, results_three.text[0:5], results_four.text]
    print(data)
    # df_two = pd.DataFrame(data, columns = ['Stock Name', 'Stock Price', '% Change'])
    x = PrettyTable()
    x.field_names = ['Stock Name', 'Stock Price', '% Change']
    x.add_row([results_two.text, results_three.text[0:5], results_four.text])

    #edited the pandas DataFrame
    # def change_percent_and_sort(df, col_name):
    #     df[col_name] = df[col_name].str.replace(r'%', '')
    #     df[col_name] = df[col_name].astype(float)
    #     return df.sort_values([col_name], ascending = False)
    #
    # df_sorted = change_percent_and_sort(df_two, '%\xa0Change')
    # df_sorted = df_sorted.rename(columns={'%\xa0Change': 'PercentChange'})


    return x.get_html_string()

if __name__ == "__main__":
    app.run(debug=True)
