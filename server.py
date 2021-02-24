import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)

db = []

@app.route("/")
def hello():
	return "Hello world!"


@app.route("/status")
def status():
	return {
		'status': True,
		'name': 'messanger',
		'time': time.time(),
		'time1': time.asctime(),
		'time2': datetime.now(),
		'time3': str(datetime.now()),
		'time4': datetime.now().strftime('%Y/%m/%d %H:%M'),
		'time5': datetime.now().isoformat(),
		'time6': datetime.utcnow().isoformat()
	}

@app.route("/send", methods = ['POST'])
def send_message():
	if not isinstance(request.json, dict):
		return abort(400)
			
	name = request.json.get('name')
	text = request.json.get('text')

	if not (isinstance(name, str) 
			and isinstance(text, str) 
			and name 
			and text):
		return abort(400)

	new_message = {
		'name': name,
		'text': text,
		'time': time.time()
	}
	db.append(new_message)

	return {'ok': True}

@app.route("/messages")
def get_messages():
	try:
		after = float(request.args.get('after', 0))
	except ValueError:
		return abort(400)

	messages = []
	for message in db:
		if message['time'] > after:
			messages.append(message)
	return {'messages': messages}

app.run()