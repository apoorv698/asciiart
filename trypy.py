# run command:
# python runServer.py
# on browser, run localhost:5010 

from flask import Flask, render_template, request, redirect, url_for, make_response
import time
import re
import cv2
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import os
import sys

app = Flask(__name__)

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}
# art = None
# title = None

@app.route('/result' , methods=['GET'])
def result():
	# global art, title
	title = request.args.get('title', None)
	art = request.args.get('art', None)
	return render_template('result.html', title=title, art=art)


@app.route('/', methods=['POST','GET'])
def index():
	# print(request.method)
	# global art, title
	if request.method == 'POST':
		title = request.form.get('title')
		# print(title)
		art = getArt(title)
		title = title.upper()
		if art:
			# print(title)
			return redirect(url_for("result",title=title,art=art))
		else:
			return render_template('result.html', error='something went wrong..')
	else:
		return render_template('index.html')

def getArt(search_word):
	imageUrl = getImageUrl(search_word)
	img = getImageContent(imageUrl)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = cv2.resize(img, (200,int(200*img.shape[0]/img.shape[1])))
	ascii_art_string = "B8&WM#YXQO{}[]()I1i!pao;:,."
	ascii_art = []
	s = ''
	for x in range(0,img.shape[0]):
		row_str = ''
		for y in range(0, img.shape[1]):
			try:
				row_str+=ascii_art_string[int(26*(img[x][y]/255))]
			except:
				pass
				# print(x,y,img[x][y])
				# pass
		# print(row_str)
		s += row_str+"\n"
	return s

def getImageUrl(search_word):
	url = 'https://www.google.com/search?hl=jp&q=' + search_word + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'
	req = urllib.request.Request(url, headers=headers)
	content = urllib.request.urlopen(req).read()
	soup = BeautifulSoup(content, 'html.parser')
	find_el = soup.find_all('img')
	txt = find_el[2]
	imageUrl = txt.get('src')
	# print(imageUrl)
	return imageUrl

def getImageContent(imageUrl):
	req = urllib.request.Request(imageUrl, headers=headers)
	imageContent = urllib.request.urlopen(req).read()
	img_array = np.array(bytearray(imageContent), dtype=np.uint8)
	# print('got image')
	img = cv2.imdecode(img_array, -1)
	return img

if __name__ =="__main__":
	debug = False
	if len(sys.argv) > 1:
		# print(True if sys.argv[1].upper() == 'TRUE' else False)
		debug = True if sys.argv[1].upper() == 'TRUE' else False
	app.run(debug=debug,port=5010)