from flask import Flask, session, render_template, request
import os
import pandas as pd
import ingest as data

app = Flask(__name__)
df = pd.read_csv('../data/college-scorecard.csv', sep=',')


@app.route('/')
@app.route('/form')
def form():
    return render_template('form.html',
                           title='Form Empty',
                           result=None)


@app.route('/form', methods=['POST'])
def form_submit():
    state = request.form['state']
    stateCount = data.getByState(state)

    return render_template('form.html',
                           title='Form Submitted',
                           result=stateCount)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run()
