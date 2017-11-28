from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
@app.route('/form')
def form():
    return render_template('form.html',
                           title='Form Empty',
                           message=None)

@app.route('/form', methods=['GET', 'POST'])
def form_submit():
    return render_template('form.html',
                           title='Form Submitted',
                           message="Success!")

if __name__ == "__main__":
    app.run()