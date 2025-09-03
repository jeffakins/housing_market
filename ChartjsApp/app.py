from flask import Flask, render_template, jsonify
import pandas as pd
import data_transform_functions as f
app = Flask(__name__)

# Input and transform housing list price data:
df_price = f.home_price_transform('data/Metro_invt_fs_uc_sfr_sm_month.csv')
print(df_price.head())

# Render HTML:
@app.route("/")
def index():
    return render_template("index.html")

# Fetch data:
@app.route("/citydata")
def get_data():
    data = {
        "dates": df_price.index.tolist(),
        "cities": {
            col: df_price[col].tolist()
            for col in df_price.columns if col != "RegionName"
        }
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)

