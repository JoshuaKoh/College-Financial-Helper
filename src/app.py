from flask import Flask, render_template, request
import os
from dataStore import *
import dropoutAnalysis
import appUtil as au
import logging
import schoolSelector
import dataOperations as do

log = logging.getLogger(__name__)

app = Flask(__name__, static_url_path="", static_folder="static")


@app.route('/')
def q_list():
    return render_template('home.html',
                           title='Question List')


@app.route('/georgia_mvp')
def georgia_mvp():
    return render_template('georgia_mvp.html',
                           title='School Finder',
                           majors=do.dfToTuple(do.majorsMap),
                           result=None)


@app.route('/georgia_mvp', methods=['POST'])
def georgia_mvp_submit():
    state = request.form['zip']
    major = request.form['majorSelect']
    sat = request.form['sat']
    act = request.form['act']
    schools = schoolSelector.selectSchools(raw_df, state, major, sat, act)

    return render_template('georgia_mvp.html',
                           title='School Finder',
                           result=schools)


@app.route('/dropout')
def dropout():
    didRun = dropoutAnalysis.run(raw_df)
    error = au.isError(not didRun, "Analysis failed to run.")

    if error:
        log.error(error)
    else:
        log.info("Successful dropout load.")

    return render_template('dropout.html',
                           title='Dropout Model',
                           error=error)


@app.route('/form')
def form():
    return render_template('form.html',
                           title='Form Empty',
                           result=None)


@app.route('/form', methods=['POST'])
def form_submit():
    state = request.form['state']
    stateCount = do.getByState(state)

    return render_template('form.html',
                           title='Form Submitted',
                           result=stateCount)


if __name__ == "__main__":
    fh = logging.FileHandler("trace.log", 'w')
    fh.setLevel(logging.INFO)
    logging.basicConfig(level="INFO")

    app.secret_key = os.urandom(24)
    app.run(debug=True)
