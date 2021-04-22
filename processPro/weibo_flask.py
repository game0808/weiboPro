from flask import Flask, render_template
from weibo_pandas import d

app = Flask(__name__)

@app.route('/')
def weibo():
    return render_template('weibo.html',d = d)

if __name__ == "__main__":
    app.run()