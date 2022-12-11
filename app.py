import pandas
import sqlalchemy
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def login_template():
    return render_template('log.html')

if __name__ == "__main__":
    app.run()