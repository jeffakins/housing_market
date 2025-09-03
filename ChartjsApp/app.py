from flask import Flask, render_template, jsonify
import pandas as pd
import data_transform_functions as f
app = Flask(__name__)

# Input and transform housing list price data:
df_price = f.home_price_transform('data/Metro_invt_fs_uc_sfr_sm_month.csv')

df = pd.DataFrame({
    "date": pd.date_range(start="2023-01-01", periods=6, freq="M"),
    "New_York_price": [100, 110, 120, 125, 130, 140],
    "LA_price": [90, 95, 100, 105, 110, 120],
    "SF_price": [80, 85, 87, 90, 95, 100],
})

# Render HTML:
@app.route("/")
def index():
    return render_template("index.html")

# Fetch data:
# @app.route("/citydata")
# def get_data():
#     data = {
#         "dates": df_price.index.tolist(),
#         "cities": {
#             col: df_price[col].tolist()
#             for col in df_price.columns if col != "RegionName"
#         }
#     }
#     return jsonify(data)


@app.route("/citydata")
def get_data():
    data = {
        "dates": df["date"].dt.strftime("%Y-%m-%d").tolist(),
        "cities": {
            col: df[col].tolist()
            for col in df.columns if col != "date"
        }
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)

