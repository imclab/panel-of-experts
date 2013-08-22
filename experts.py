import os
from flask import Flask, request, send_file
from flask import jsonify
import Image
import urllib2 as urllib
import io
import cStringIO

from lib.shannon import *

app = Flask(__name__)

@app.route('/shannon', methods=['GET', 'POST'])
def shannon():
	imagedata = request.files['imagedata']		
	im = Image.open(imagedata)

	shannon = shannon_entropy(im)
		
	return jsonify(stat="ok", shannon=shannon)	
		
		
@app.route('/shannon/region', methods=['GET', 'POST'])
def shannon_region():		
	imagedata = request.files['imagedata']		
	im = Image.open(imagedata)
	
	shannon_region = sliced_shannon(im)
	return jsonify(stat="ok", shannon_region=shannon_region)
	
@app.route('/shannon/region/web', methods=['GET', 'POST'])
def shannon_region_web():
	url = request.args.get('url')
	imagedata = urllib.urlopen(url)
	image_file = io.BytesIO(imagedata.read())
	
	im = Image.open(image_file)
	shannon_region = sliced_shannon(im)
	x = shannon_region['x'] - 100
	y = shannon_region['y'] - 100
	mx = shannon_region['x'] + 200
	my = shannon_region['y'] + 200
	
	thumb = im.crop((x, y, mx, my))
	
	img_io = cStringIO.StringIO()
	thumb.save(img_io, 'JPEG', quality=70)
	img_io.seek(0)
	return send_file(img_io, mimetype='image/jpeg')
			
	
		