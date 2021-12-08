from flask import Flask, json, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, Request
from prettytable import PrettyTable
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
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

@app.route('/_top_stocks/', methods=['GET'])
def TopStocks():
    df_sorted = sorted_df()
    # top_stocks = df_sorted['Company'][:10].array
    df_sorted['Company'] = [arr[1] for arr in df_sorted['Company'].str.split(' ', 1)]
    top_stocks = df_sorted[:10]
    # top_stocks = top_stocks.reset_index()
    # top_stocks.index += 1

    x = PrettyTable()
    x.field_names = ["Company"]
    for row in top_stocks.itertuples(index=True, name='Pandas'):
        print(row.count)
        x.add_row([row.Company])
    # print(x)
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

    message = {"Headline": headlines, "links": links}

    df_links = pd.DataFrame(message)
    top_sentiments = SentimentAnalysis(df_links)

    return top_sentiments.to_html()

    # top_sent = PrettyTable()
    # top_sent.field_names = ["Headline", "Sentiment"]
    # for row in top_sentiments.itertuples(index=True, name='Pandas'):
    #     # print(row.count)
    #     top_sent.add_row([row.Headline, row.Sentiment])
    #
    # # print(top_sent)
    # return top_sent.get_html_string()
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

def LinksForSentimentAnalysis(stockURL):
   page_two  = requests.get(stockURL)
   soup_three = BeautifulSoup(page_two.content, "html.parser")
   results_five = soup_three.find_all("td", class_="firstCol")
   df_three = pd.DataFrame(columns = ['Headlines'])
   for result in results_five:
    links = result.find_all("a")
    for link in links:
        data_two = link.text.strip()
        df_three = df_three.append({'Headlines': data_two}, ignore_index=True)

    return df_three

# @app.route('/_sentiment_analysis/', methods=['GET'])
def Sentiment_Analysis_perstock():
    stockURL = "https://money.cnn.com/quote/quote.html?symb=LUV"
    parsed_df = LinksForSentimentAnalysis(stockURL)
    sentiment_df = SentimentAnalysis(parsed_df)
    sentiment = sentiment_df.Sentiment.mode()[0]
    return sentiment

@app.route('/_visualize/', methods=['GET'])
def Visualize():
    # #plot a bar graph of top 5 stocks
    matplotlib.use('agg')
    df_sorted = sorted_df()
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(df_sorted['Company'][:5],df_sorted['PercentChange'][:5])
    plt.xticks(rotation = 45) # Rotates X-Axis Ticks by 45-degrees
    plt.title("Top 5 Stocks Bar Chart")
    plt.savefig('CourseProject/topstocks.png', format="png")
    # plt.show()
    #
    # #plot only positive increasing stocks
    # plt.scatter(df_sorted.Price[:5], df_sorted.PercentChange[:5])
    # plt.title("Percent Change vs Price for Top 5 Stocks")
    # plt.xlabel("Price")
    # plt.ylabel("Percent Change")
    # plt.show()
    # plt.savefig('path/to/pic.png')

    #sentiment analysis plot for top 10 stocks
    # df_sorted = sorted_df()
    # parsed_stocks = SentimentAnalysis(df_sorted)
    # grouped_stocks = parsed_stocks.groupby('Sentiment').count()
    # grouped_stocks.reset_index(level=0, inplace=True)
    # fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    # ax.bar(grouped_stocks.Sentiment,grouped_stocks.Positive)
    # plt.xticks(rotation = 45) # Rotates X-Axis Ticks by 45-degrees
    # plt.title("Sentiment Analysis Bar Chart")
    # # plt.show()
    # # mpld3.show()
    # plt.savefig('sentimentAnalysis.png')
    # plt.show()

    # return parsed_stocks.to_html()

if __name__ == "__main__":
    app.run(debug=True)
