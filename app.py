from flask import Flask
from flask import render_template
from flask import url_for

app = Flask(__name__)

# $ export FLASK_APP=app.py
# $ flask run

@app.route('/')
@app.route('/form')
def form():
    return render_template('form.html',
                           title='Form Empty',
                           message=None)

@app.route('/form')
def form_submit():
    return render_template('form.html',
                           title='Form Submitted',
                           message="Success!")