from flask import render_template, app


@app.route("/")
def index():
    to_send=database()
    return render_template("Visuell.html", to_send=to_send)