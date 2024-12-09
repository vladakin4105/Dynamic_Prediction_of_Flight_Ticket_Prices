from flask import Flask, request, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
	app.run(debug=True)
