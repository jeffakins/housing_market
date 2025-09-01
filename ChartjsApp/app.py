from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Example DataFrames
df_participants = pd.DataFrame({
    "date": pd.date_range(start="2023-01-01", periods=10, freq="M"),
    "planned": [100, 120, 140, 160, 180, 200, 220, 210, 230, 250],
    "actual": [90, 115, 135, 150, 175, 190, 210, 200, 220, 240]
})

df_revenue = pd.DataFrame({
    "date": pd.date_range(start="2023-01-01", periods=10, freq="M"),
    "forecast": [1000, 1200, 1250, 1300, 1400, 1600, 1800, 1750, 1850, 2000],
    "actual": [950, 1100, 1230, 1280, 1350, 1500, 1700, 1680, 1800, 1950]
})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data/participants")
def get_participants_data():
    data = {
        "date": df_participants["date"].dt.strftime("%Y-%m-%d").tolist(),
        "planned": df_participants["planned"].tolist(),
        "actual": df_participants["actual"].tolist()
    }
    return jsonify(data)

@app.route("/data/revenue")
def get_revenue_data():
    data = {
        "date": df_revenue["date"].dt.strftime("%Y-%m-%d").tolist(),
        "forecast": df_revenue["forecast"].tolist(),
        "actual": df_revenue["actual"].tolist()
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

