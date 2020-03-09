from flask import Flask, render_template, request, url_for
from search import search_result
import os

# http://127.0.0.1:5000/

app = Flask(__name__)

@app.route('/')
@app.route('/home', methods=["POST"])
def home():
    return render_template("home.html") # can also return html


@app.route('/', methods=["GET","POST"])
def result():
    queries = request.form["queries"]
    num_of_result = int(request.form["numOfResults"])
    print(num_of_result)
    results = search_result(queries, num_of_result)[:-1]
    actual_results = len(results)
    time = search_result(queries, num_of_result)[-1]
    return render_template("result.html", queries=queries, results=results, time=time, num_of_result=num_of_result, actual_results=actual_results)

if __name__ == "__main__":
    app.run(debug=True)
