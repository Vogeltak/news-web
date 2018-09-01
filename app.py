from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import jsonify
import json
from datetime import datetime

app = Flask(__name__)

def get_articles():
	with open('/var/www/news/data.json', 'r') as f:
		data = json.load(f)	

	data.sort(key=lambda x: x['date'], reverse=True)

	for a in data:
		a['date'] = datetime.strptime(a['date'], '%Y-%m-%d %H:%M:%S').strftime('%B %d, %Y') 

	return data

@app.route('/')
def list():
	return render_template('list.html', articles=get_articles())

@app.route('/article/<int:id>')
def article(id):
	data = get_articles()
	if id >= 0 and id < len(data):
		return render_template('article.html', a=data[id])
	return redirect(url_for('list'))

# API functionality
@app.route('/api/v1/articles')
def api_articles():
	with open('/var/www/news/data.json', 'r') as f:
		data = json.load(f)
	
	return jsonify(data)
