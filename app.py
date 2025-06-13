from flask import Flask, render_template, request, redirect, url_for
from analysis import run_analysis
import webbrowser
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("analyze"))

@app.route("/analyze")
def analyze():
    faculty_list = ['Prof. Antonio', 'Prof. Miranda', 'Prof. Valdez', 'Prof. Enriquez', 'Prof. Santiago']
    return render_template("results.html", faculty_list=faculty_list, table=None)

@app.route("/analyze/faculty", methods=["GET"])
def filter_by_faculty():
    selected = request.args.get("faculty")
    df = run_analysis(prof_name=selected)
    table_html = df.to_html(classes='table table-striped', index=False)
    faculty_list = ['Prof. Antonio', 'Prof. Miranda', 'Prof. Valdez', 'Prof. Enriquez', 'Prof. Santiago']
    return render_template("results.html", faculty_list=faculty_list, table=table_html)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/analyze")

#  For development purposes, uncomment the following lines to open the browser automatically
# if __name__ == "__main__":
#     threading.Timer(1.25, open_browser).start()
#     app.run(debug=False)

# For production, use the following lines to run the Flask app without opening the browser automatically
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
