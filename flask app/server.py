from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

@app.route('/_top_stocks/')
def TopStocks():
    URL = "https://money.cnn.com/data/hotstocks/index.html"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="wsod_dataTable wsod_dataTableBigAlt")
    df = pd.read_html(str(results))[0]
    return jsonify(df.to_string())

@app.route('/stock', methods=['GET'])
def SpecificStock():
    stockURL = request.args.get('url')
    page_two = requests.get(stockURL)

    soup_two = BeautifulSoup(page_two.content, "html.parser")

    results_two = soup_two.find("h1",class_="wsod_fLeft")
    results_three = soup_two.find("td",class_="wsod_last")
    results_four = soup_two.find("span",class_="posData")

    data = [[results_two.text,results_three.text[0:5], results_four.text]]
    df_two = pd.DataFrame(data, columns = ['Stock Name', 'Stock Price', '% Change'])
    return jsonify(df_two.to_string())

if __name__ == "__main__":
    app.run(debug=True)