import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient("mongodb+srv://sparta:test@cluster0.nvtjoqu.mongodb.net/?retryWrites=true&w=majority")
db = client.pirates_lv1

url = 'https://korean.visitseoul.net/exhibition/SEOUL-VIBE/KOP6w9tgb'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

title = soup.select_one('#container > div.wide-inner > section > h3').text
period = soup.select_one('#container > div.detial-cont-element.active > div > dl:nth-child(1) > dd').text.strip()
tags = soup.select_one('#container > section.tag-element.poi > p').text.replace('\n',' ')

image = soup.select('.item')[1]['style'].replace("background-image:url('",'').replace("');",'')
image = 'https://korean.visitseoul.net'+image

doc = {
    'title':title,
    'period':period,
    'tags':tags,
    'image':image
}

db.exhibition.insert_one(doc)