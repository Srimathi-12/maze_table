import pymongo
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import datetime
import re
from dateutil import parser
from dateutil.parser import ParserError
from pymongo import ASCENDING, DESCENDING
import re   

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['CDAT']  # Replace 'your_database' with your actual database name
collection = db['raw_data']  # Replace 'your_collection' with your actual collection name

@app.route('/search', methods=['POST'])
def search():
    search_queries = request.json
    input_value = search_queries['input_value']
    page = search_queries['page']
    items_per_page = search_queries['items_per_page']
    distinct_key = search_queries['distinct_key']
    search_params = search_queries['search_params']
    selected_checkboxes = search_queries['selected_checkboxes']
    print(search_params,"search_params")

    filtered_data = []
    total_filter = []
    total_data = []
    checkbox_query = {}
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    total_data = list(collection.find({'msisdn':input_value}, {'_id': 0}))

    # Applying filters based on selected checkboxes
    filters = []
    for key, values in selected_checkboxes.items():
        filters.append({key: {"$in": [str(value) for value in values]}})

    if filters:
        filter_query = {"$and": filters}  
        total_filter = list(collection.find({"$and": [{'msisdn': input_value}, filter_query]}, {'_id': 0}))
        filtered_data = list(collection.find({"$and": [{'msisdn': input_value}, filter_query]}, {'_id': 0}).sort('_id').skip(start_index).limit(items_per_page))
    else:
        total_filter = list(collection.find({'msisdn': input_value}, {'_id': 0}))
        filtered_data = list(collection.find({'msisdn': input_value}, {'_id': 0}).sort('_id').skip(start_index).limit(items_per_page))

    total_len = len(total_filter)
    
   # Finding unique values for each key in distinct_key
    unique_values = {}
    for key in distinct_key:
        unique_values[key] = set()

    for data in total_data:
        for key in distinct_key:
            if key in data:
                unique_values[key].add(data[key])

    # Convert sets to lists
    for key, values in unique_values.items():
        unique_values[key] = list(values)
     
     # Filtering unique values based on search parameters
    for key, value in search_params.items():
        if key in unique_values:
            unique_values[key] = [v for v in unique_values[key] if value in str(v)]

     # Applying additional filtering based on selected checkboxes
    for key, values in selected_checkboxes.items():
        if key in distinct_key:
            filtered_data = [data for data in filtered_data if data.get(key) in values]
    
    # filtered_data = list(collection.find({input_field_name:input_value}, {'_id': 0}).sort('_id').skip(start_index).limit(items_per_page))
    
    return jsonify({"data": filtered_data,"total": total_len,"unique_values":unique_values})

if __name__ == '__main__':
    app.run(debug=True)

