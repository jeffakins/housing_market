from flask import Flask, jsonify, render_template, request
import pandas as pd
import data_transform_functions as f

# Initialize the Flask application
app = Flask(__name__)

# Input and transform housing list price data:
df_price = f.home_price_inventory_transform('data/Metro_mlp_uc_sfr_sm_month.csv') # Mean list price SFH
df_inv = f.home_price_inventory_transform('data/Metro_invt_fs_uc_sfr_sm_month.csv') # Inventory

# --- Chart Data ---
# This data is now managed by the backend.# --- Color Palette for Chart Lines ---
# --- Color Palette for Chart Lines ---
# A list of colors to cycle through for different cities.
COLOR_PALETTE = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
    '#FF9F40', '#C9CBCF', '#7CFFB2' 
]

@app.route('/')
def home():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/cities')
def get_cities():
    """Provides the list of available cities."""
    return jsonify(list(df_price.columns))

@app.route('/api/citydata')
def get_chart_data():
    """
    Provides chart data as JSON based on selected cities from query parameters.
    Example request: /api/data?cities=New York,Los Angeles
    """
    # Get the cities that the user selects:
    selected_cities_str = request.args.get('cities')
    
    if not selected_cities_str:
        return jsonify({"error": "No cities selected"}), 400
        
    # Format the city strings to match the dataset format    
    # 1. Split by all commas
    split_by_all_commas = selected_cities_str.split(',')
    # 2. Group elements in pairs
    paired_elements = zip(split_by_all_commas[::2], split_by_all_commas[1::2])
    # 3. Join the pairs with a comma in between
    selected_cities = [f"{first},{second}" for first, second in paired_elements]

    # Filter the DataFrame to include only the selected cities
    filtered_df = df_price[selected_cities]
    
    chart_data = {
        'labels': list(filtered_df.index),
        'datasets': []
    }
    
    # Create a dataset for each selected city
    for i, city in enumerate(filtered_df.columns):
        dataset = {
            'label': city,
            'data': list(filtered_df[city]),
            'fill': False,
            'borderColor': COLOR_PALETTE[i % len(COLOR_PALETTE)], # Cycle through colors
            'tension': 0.1,
            'borderWidth': 3,
            'pointRadius': 4,
            'pointHoverRadius': 7
        }
        chart_data['datasets'].append(dataset)
       
    return jsonify(chart_data)

if __name__ == '__main__':
    # Run the app in debug mode.
    app.run(debug=True)

