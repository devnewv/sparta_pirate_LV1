#client = MongoClient("mongodb+srv://sparta:test@cluster0.nvtjoqu.mongodb.net/?retryWrites=true&w=majority")

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient("mongodb+srv://sparta:test@cluster0.nvtjoqu.mongodb.net/?retryWrites=true&w=majority")
db = client.pirates_lv1

@app.route('/')
def home():
	return render_template("index.html")


@app.route('/exhibit', methods=["POST"])
def post_exhibit():
    url_receive = request.form["url_give"]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('#container > div.wide-inner > section > h3').text
    period = soup.select_one('#container > div.detial-cont-element.active > div > dl:nth-child(1) > dd').text.strip()
    tags = soup.select_one('#container > section.tag-element.poi > p').text.replace('\n',' ')

    image = 'https://korean.visitseoul.net/'+soup.select('.item')[1]['style'].split('(')[1].replace(');','').replace('\'','')

    doc = {
        'title':title,
        'period':period,
        'tags':tags,
        'image':image,
        'url':url_receive
    }

    db.exhibition.insert_one(doc)

    return jsonify({"msg": "저장 완료!"})

@app.route('/exhibit', methods=["GET"])
def get_exhibit():
    exhibitions = list(db.exhibition.find({},{'_id':False}))
    return jsonify({'exhibitions':exhibitions})

@app.route('/now', methods=["GET"])
def get_now():
    url = 'https://korean.visitseoul.net/exhibition'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    items = soup.select('.item > a')
    base = 'https://korean.visitseoul.net'

    docs = []
    for item in items:
        url = base+item['href']
        image = base+item.select_one('.thumb')['style'].split('(')[1].replace(')','')
        title = item.select_one('.title').text
        period = item.select_one('.small-text.text-dot-d').text.strip()
        doc = {
            'url':url,
            'image':image,
            'title':title,
            'period':period
        }
        docs.append(doc)

    return jsonify({'now':docs})

if __name__ == "__main__":
	app.run(debug=True, port=8080)