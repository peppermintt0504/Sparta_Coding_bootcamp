import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.dbsparta


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20220101',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# 코딩 시작

title = soup.select('#old_content > table > tbody > tr')

for tr in title:
    a_rank = tr.select_one('td.ac > img')
    a_tag = tr.select_one('td.title > div > a')
    a_point = tr.select_one('td.point')

    if a_tag is not None:
        print(a_rank['alt'] + " " + a_tag.text + " " + a_point.text)
        doc = {
            'rank': a_rank['alt'],
            'title': a_tag.text,
            'star': a_point.text
        }
        db.movies.insert_one(doc)


