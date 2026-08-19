from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def homaPage():
    return render_template("homePage.html")

if __name__ == "__main__":
    app.run(debug=True)
