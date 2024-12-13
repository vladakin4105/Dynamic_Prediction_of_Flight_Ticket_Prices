from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import asyncio
import websockets
import time
import threading
import logging
import web_test

logging.getLogger('werkeug').setLevel(logging.ERROR)

app = Flask(__name__)

CORS(app)

progress = 1
solution = -1

@app.route('/')

def home():
	return render_template('home.html')

@app.route('/home')
def go_back():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/services')
def services():
    return render_template('services.html')

def progress_update(value):
     global progress
     progress = value

def solution_update(value):
     global solution
     solution = round(value,2)

@app.route('/start_task', methods=['POST'])
def start_task():
    global progress 
    global solution
    data = request.get_json()
    #print(f"Received data: {data}")
    from_location = data.get('origin')
    to_location = data.get('destination')
    pred_date = data.get('departure_date')
    print("Before calling web_test.main")
    #web_test.main(from_location,to_location,pred_date,progress_update)
    threading.Thread(
         target=web_test.main,args=(from_location,to_location,pred_date,progress_update,solution_update)
         ).start()
    progress=1
    return jsonify({"message": "Task started"})

@app.route('/get_progress', methods = ['GET'])
def get_progress():
    global progress
    return jsonify({
         "progress": progress
                    })

@app.route('/get_solution', methods = ['GET'])
def get_solution():
     global solution
     return jsonify({
         "solution": solution
     })




if __name__ == '__main__':
	app.run(debug=False, threaded= True ,host="127.0.0.1", port=5000)




