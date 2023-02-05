from flask import render_template, Flask

app = Flask(__name__)


@app.route("/")
def index():
    to_send = [1,2,3]
    return render_template("Visuell.html", chart_data = [1,2,3,4,5])