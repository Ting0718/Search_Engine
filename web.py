from flask import Flask, render_template, request
from search import search_result

# http://127.0.0.1:5000/

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")# can also return html


@app.route('/', methods=["GET","POST"])
def result():
    queries = request.form["queries"]
    top_five_urls = search_result(queries)[:-1]
    time = search_result(queries)[-1]
    return render_template("result.html",queries=queries,top_five_urls=top_five_urls, time = time)

if __name__ == "__main__":
    app.run(debug=True)
