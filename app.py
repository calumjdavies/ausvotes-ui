from flask import Flask, render_template


app = Flask(__name__, static_folder="static")


@app.route("/")
@app.route("/home")
def root():
    return render_template("index.html")

@app.route("/elections")
def elections():
    return render_template("elections.html")

@app.route("/elections/<id>")
def election(id):
    return f"Results for election {id}"

@app.route("/candidates")
def candidates_all():
    return render_template("candidates.html")

@app.route("/pollingplaces")
def pollingplaces():
    return render_template("polling_places.html")
