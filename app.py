from flask import Flask, request, jsonify, render_template,redirect,flash,send_file,url_for
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

#load model
model = pickle.load(open('rf.pkl', 'rb'))

app = Flask(__name__)
app.secret_key=('secret_key')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='validate'
mysql=MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign')
def sign():
	return render_template('signup.html')
@app.route('/signup', methods=['GET','POST']) 
def signup():
	msg=''
	if request.method=='POST':
		username=request.form['uname']
		password=request.form['password']
		email=request.form['email']
		password2=request.form['pwd2']
		
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM signin WHERE username=%s',(username,))
		account=cursor.fetchone()
		if account:
			msg='Account already exists!'
			return render_template('signup.html',msg=msg)
		elif password !=password2:
			msg='Passwords do not match!'
			return render_template('signup.html',msg=msg)
		else:
			cursor.execute('INSERT INTO signin VALUES(NULL, %s, %s, %s)', (username,password,email,))
			mysql.connection.commit()
			return redirect(url_for('login'))



@app.route('/login2', methods=['POST'])
def login2():
	msg=''
	if request.method=='POST':
		username=request.form['uname']
		password=request.form['pwd']
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM signin WHERE username=%s AND password =%s',(username,password,))
		user=cursor.fetchone()
		if user:
			print("Login success")
			return redirect(url_for('upload'))
		else:
			msg='Invalid Login! Plz Try Again!'
			print(msg)
			return render_template('login.html',msg=msg)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/preview',methods=["POST"])
def preview():
    if request.method == 'POST':
        dataset = request.files['dataset']
        df = pd.read_csv(dataset,encoding = 'unicode_escape')
        df.set_index('Id', inplace=True)
        return render_template("preview.html",df_view = df)	

@app.route('/prediction',methods=['GET', 'POST'])
def prediction():
    return render_template('prediction.html')

@app.route('/predict',methods=['POST'])
def predict():
    feature = [x for x in request.form.values()]
    print("Input features:", feature)
    
    # Convert the input features to the correct format (pandas DataFrame)
    columns = ['location', 'bedroom', 'total_sqft', 'bath', 'balcony','price_per_sqft']  # Ensure these are in the correct order
    input_data = pd.DataFrame([feature], columns=columns)
    
    # Predict the result using the loaded model
    result = model.predict(input_data)
    return render_template('prediction.html', prediction_text= result)

@app.route('/performance')
def performance():
	return render_template('performance.html')  

@app.route('/chart')
def chart():
	return render_template('chart.html')  

if __name__ == "__main__":
    app.run(debug=True)