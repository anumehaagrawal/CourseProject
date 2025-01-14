from flask import Flask, json, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, Request
from prettytable import PrettyTable
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import matplotlib
import mpld3
from mpld3 import plugins

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

def sorted_df():
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
    return df_sorted

def SentimentAnalysis(dataframe):
    parsed_stocks = dataframe

    #sentiment analysis
    results = []
    for headline in parsed_stocks['Headline']:
        polarity_score = SentimentIntensityAnalyzer().polarity_scores(headline)
        polarity_score['headline'] = headline
        results.append(polarity_score)
    parsed_stocks['Score'] = pd.DataFrame(results)['compound']

    #add sentiment column
    sentiment = []
    for val in parsed_stocks['Score']:
        if val == 0:
            sentiment.append('Neutral')
        elif val > 0:
            sentiment.append('Positive')
        else:
            sentiment.append('Negative')
    parsed_stocks['Sentiment'] = sentiment
    df_sentiment = parsed_stocks[['Headline', 'Sentiment']]
    df_sentiment.index += 1

    return df_sentiment

def Top_News_Parser():
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

    html = html.find_all(class_="thumb-caption")

    headlines = []
    for headline in html:
        headlines.append(headline.text.strip())

    message = {"Headline": headlines, "links": links}

    df_links = pd.DataFrame(message)
    top_sentiments = SentimentAnalysis(df_links)
    return top_sentiments


@app.route('/_top_stocks/', methods=['GET'])
def TopStocks():
    df_sorted = sorted_df()
    df_sorted['Company'] = [arr[1] for arr in df_sorted['Company'].str.split(' ', 1)]
    top_stocks = df_sorted[:10]
    top_stocks = top_stocks.reset_index()
    top_stocks.index += 1
    top_stocks['Index'] = top_stocks.index

    x = PrettyTable()
    x.field_names = [" ", "Company", "Price", "Percent Change"]
    for row in top_stocks.itertuples(index=True, name='Pandas'):
        x.add_row([row.Index, row.Company, row.Price, row.PercentChange])

    return x.get_html_string(attributes={"class":"styled-table"})


@app.route('/_top_stocks_news/', methods=['GET'])
def TopNewsInfo():
    top_sentiments = Top_News_Parser()
    x = PrettyTable()
    x.field_names = ["Headline", "Sentiment"]
    for row in top_sentiments.itertuples(index=True, name='Pandas'):
        x.add_row([row.Headline, row.Sentiment])

    return x.get_html_string(attributes={"class":"styled-table"})

@app.route('/stock', methods=['GET'])
def SpecificStock():
    stockURL = request.args.get('url')
    page_two = requests.get(stockURL)

    soup_two = BeautifulSoup(page_two.content, "html.parser")

    results_two = soup_two.find("h1",class_="wsod_fLeft")
    results_three = soup_two.find("td",class_="wsod_last")
    results_four = soup_two.find("span",class_="posData")

    parsed_df = LinksForSentimentAnalysis(stockURL)
    sentiment_df = SentimentAnalysis(parsed_df)
    sentiment = sentiment_df.Sentiment.mode()[0]

    data = [results_two.text, results_three.text[0:5], results_four.text, sentiment]
    x = PrettyTable()
    x.field_names = ['Stock Name', 'Stock Price', 'Percent Change', 'Sentiment']
    x.add_row([results_two.text, results_three.text[0:5], results_four.text, sentiment])

    return x.get_html_string(attributes={"class":"styled-table"})

def LinksForSentimentAnalysis(stockURL):
   page_two  = requests.get(stockURL)
   soup_three = BeautifulSoup(page_two.content, "html.parser")
   results_five = soup_three.find_all("td", class_="firstCol")
   df_three = pd.DataFrame(columns = ['Headline'])
   for result in results_five:
    links = result.find_all("a")
    for link in links:
        data_two = link.text.strip()
        df_three = df_three.append({'Headline': data_two}, ignore_index=True)

    return df_three

@app.route('/sentiment', methods=['GET'])
def Sentiment_Analysis_perstock():
    stockURL = request.args.get('url')
    parsed_df = LinksForSentimentAnalysis(stockURL)
    sentiment_df = SentimentAnalysis(parsed_df)
    sentiment = sentiment_df.Sentiment.mode()[0]
    return sentiment


@app.route('/visualize/', methods=['GET'])
def Visualize():
    matplotlib.use('agg')
    df_sorted = sorted_df()
    df_sorted['Company'] = [arr[1] for arr in df_sorted['Company'].str.split(' ', 1)]

    #save top 5 stocks bar graph into an image
    fig = plt.figure(figsize=(8, 8)) #8 x 8
    plt.bar(df_sorted['Company'][:5],df_sorted['PercentChange'][:5])
    plt.xticks(rotation = 15) # Rotates X-Axis Ticks by 15-degrees
    plt.title("Top 5 Stocks Bar Chart")
    plt.ylabel("Percent Change")
    plt.savefig('../sample_extension/topstocks.png', format="png")


    return "Top Stock Visualization:"

@app.route('/visualize1/', methods=['GET'])
def Visualize1():
    matplotlib.use('agg')
    top_sentiments = Top_News_Parser()
    grouped_stocks = top_sentiments.groupby('Sentiment').count()
    grouped_stocks.reset_index(level=0, inplace=True)

    #save price versus percent change scatter plot into an image
    fig1 = plt.figure(figsize=(8, 8))
    plt.bar(grouped_stocks.Sentiment,grouped_stocks.Headline)
    plt.xticks(rotation = 15) # Rotates X-Axis Ticks by 15-degrees
    plt.title("Sentiment Analysis Bar Chart")
    plt.ylabel("Count")
    plt.savefig('../sample_extension/sentimentgraph.png', format="png")

    return "Sentiment Visualization:"

if __name__ == "__main__":
    app.run(debug=True)
