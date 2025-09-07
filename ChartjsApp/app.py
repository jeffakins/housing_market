# from flask import Flask, render_template, jsonify
# import pandas as pd
# import data_transform_functions as f
# app = Flask(__name__)






from flask import Flask, jsonify, render_template
import pandas as pd
import data_transform_functions as f

# Initialize the Flask application
app = Flask(__name__)

# Input and transform housing list price data:
df_price = f.home_price_transform('data/Metro_invt_fs_uc_sfr_sm_month.csv')
print(df_price.info())
print(df_price.index.dtype)

# --- Chart Data ---
# This data is now managed by the backend.
chart_data = {
    'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'],
    'datasets': [{
        'label': 'Sample Dataset A (from Backend)',
        'data': [65, 59, 80, 81, 56, 55, 40, 60],
        'fill': False,
        'borderColor': 'rgb(75, 192, 192)',
        'tension': 0.4,
        'borderWidth': 3,
        'pointBackgroundColor': 'rgb(75, 192, 192)',
        'pointRadius': 5,
        'pointHoverRadius': 8
    },
    {
        'label': 'Sample Dataset B (from Backend)',
        'data': [28, 48, 40, 19, 86, 27, 90, 75],
        'fill': False,
        'borderColor': 'rgb(255, 99, 132)',
        'tension': 0.4,
        'borderWidth': 3,
        'pointBackgroundColor': 'rgb(255, 99, 132)',
        'pointRadius': 5,
        'pointHoverRadius': 8
    }]
}

@app.route('/')
def home():
    """Serves the main HTML page."""
    # Flask will look for this file in the 'templates' folder.
    return render_template('index.html')

@app.route('/data')
def get_chart_data():
    """Provides the chart data as JSON."""
    return jsonify(chart_data)

if __name__ == '__main__':
    # Run the app in debug mode.
    app.run(debug=True)
