from flask import Flask

app = Flask(__name__)
@app.route('/')

def hello_world():
	return 'Flask en una caja de Vagrant\n'
if __name__ == '__main__':
	app.run(host='0.0.0.0')
