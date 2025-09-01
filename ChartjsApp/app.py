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
@app.route("/housedata")
def get_data():
    data = {
        "dates": df_price.index.tolist(),
        "cities": {
            col: df_price[col].tolist()
            for col in df_price.columns if col != "RegionName"
        }
    }
    return jsonify(data)


# @app.route("/data/participants")
# def get_participants_data():
#     data = {
#         "date": df_participants["date"].dt.strftime("%Y-%m-%d").tolist(),
#         "planned": df_participants["planned"].tolist(),
#         "actual": df_participants["actual"].tolist()
#     }
#     return jsonify(data)

# @app.route("/data/revenue")
# def get_revenue_data():
#     data = {
#         "date": df_revenue["date"].dt.strftime("%Y-%m-%d").tolist(),
#         "forecast": df_revenue["forecast"].tolist(),
#         "actual": df_revenue["actual"].tolist()
#     }
#     return jsonify(data) 

# # Getting data using Pandas df
# @app.route('/data', methods=['GET'])
# def get_data():
#     return jsonify(df_price.to_dict(orient="records"))  # Serves the JSON data

if __name__ == "__main__":
    app.run(debug=True)

