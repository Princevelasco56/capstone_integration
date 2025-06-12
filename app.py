from flask import Flask, render_template
from analysis import run_analysis

app = Flask(__name__)

@app.route("/analyze")
def analyze():
    df = run_analysis()
    table_html = df.head(10).to_html(classes='table table-striped', index=False)
    return render_template("results.html", table=table_html)

if __name__ == "__main__":
    app.run(debug=True)
