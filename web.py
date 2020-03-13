from flask import Flask, render_template, request, url_for
from search import search_result_cosine, search_result
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

    if request.method == "POST":
        sort = request.form['sort']

    if sort == "cosine similarity":
        output = search_result_cosine(queries.split(), num_of_result)
        results = output[:-1]
        actual_results = len(results)
        time = output[-1]

    elif sort == "tf-idf": # still need to change to tf-idf
        output = search_result(queries, num_of_result)
        results = output[:-1]
        actual_results = len(results)
        time = output[-1]
   
    return render_template("result.html", queries=queries, results=results, time=time, num_of_result=num_of_result, actual_results=actual_results, sort=sort)
    #return render_template("result.html", queries=queries, results=results, num_of_result=num_of_result, actual_results=actual_results)

if __name__ == "__main__":
    app.run(debug=True)
