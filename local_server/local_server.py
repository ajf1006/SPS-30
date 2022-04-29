from flask import Flask,request,render_template
import sqlite3

app = Flask(__name__)

@app.route('/receive-data')

def receive_data():
	'''
	Receives the data from sensor and inserts it into the data-base.
	'''
	date = request.args.get('date')
	time = request.args.get('time')
	pm2pt5 = request.args.get('pm2pt5')
	pm10 = request.args.get('pm10')

	
	con = sqlite3.connect('particulates.db')
	cur = con.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS particulates (id int, date text,time text, pm10 real, pm2pt5 real)''')
	
	cur.execute('''SELECT COUNT(*) FROM particulates''')
	counts = cur.fetchall()[0][0]
	print(counts)
	if counts == 0:
		current_id = 1
	else:
		cur.execute('SELECT * FROM particulates ORDER BY id DESC LIMIT 1')
		current_id = cur.fetchall()[0][0]+1
		print(current_id)

	cur.execute('SELECT EXISTS(SELECT 1 FROM particulates WHERE date=? AND time=?)',(date,time))
	exists = cur.fetchall()[0][0]
	if exists == 0:
		cur.execute("INSERT INTO particulates VALUES (?,?,?,?,?)",(current_id,date,time,pm10,pm2pt5))
		con.commit()
	con.close()
	return '<h1>Data Received</h1>'


@app.route('/read-data')
def read_data():
	'''
	Reads the database, finds the latest data and renders it as html.
	'''
	con = sqlite3.connect('particulates.db')
	cur = con.cursor()

	cur.execute('SELECT * FROM particulates')
	print(cur.fetchall())
	cur.execute('SELECT * FROM particulates ORDER BY id DESC LIMIT 1')
	data = cur.fetchall()[0]
	date = data[1]
	time = data[2]
	pm10 = data[3]
	pm2pt5 = data[4]
	con.close()

	return render_template('hello.html',date = date,time = time,pm2pt5 = pm2pt5,pm10 = pm10)