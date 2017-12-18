from flask import Flask, render_template, request
import os
import pandas as pd
import ingest as data
import dropoutAnalysis
import appUtil as AU
import logging

log = logging.getLogger(__name__)

app = Flask(__name__)
df = pd.read_csv('../data/college-scorecard.csv', sep=',',
                 dtype={'ZIP': str,
                        'NPCURL': str,
                        'C150_L4_POOLED_SUPP': str,
                        'C150_4_POOLED_SUPP': str,
                        'C200_L4_POOLED_SUPP': str,
                        'C200_4_POOLED_SUPP': str,
                        'ALIAS': str,
                        'T4APPROVALDATE': str
                        })


@app.route('/')
def q_list():
    return render_template('home.html',
                           title='Question List')


@app.route('/georgia_mvp')
def georgia_mvp():
    return render_template('georgia_mvp.html',
                           title='Schools Near Me',
                           result=None)


@app.route('/georgia_mvp', methods=['POST'])
def georgia_mvp_submit():
    state = request.form['state']
    major = request.form['major']
    dataByState = data.getByState(state, major)

    error = AU.isError(dataByState.empty, "That's not a state code. Please try again.")

    html = ""
    for index, school in dataByState.iterrows():
        html += "<a href='" + school['INSTURL'] + "'>"
        html += "<h3>" + school['INSTNM'] + "</h3>" + "</a>"
        html += school['CITY'] + ", " + school['STABBR'] + " " + school['ZIP'] + "<br/>"
        html += "<i>SAT average: " + str(school['SAT_AVG_ALL']) + "</i><br/>"
        html += "-----<br/>"

    return render_template('georgia_mvp.html',
                           title='Schools Near Me Submitted',
                           error=error,
                           result=html)


@app.route('/dropout')
def dropout():
    didRun = dropoutAnalysis.run(df)
    error = AU.isError(not didRun, "Analysis failed to run.")

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
    stateCount = data.getByState(state)

    return render_template('form.html',
                           title='Form Submitted',
                           result=stateCount)


if __name__ == "__main__":
    fh = logging.FileHandler("trace.log", 'w')
    fh.setLevel(logging.INFO)
    logging.basicConfig(level="INFO")

    app.secret_key = os.urandom(24)
    app.run(debug=True)
