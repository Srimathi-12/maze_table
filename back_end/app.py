import pymongo
import datetime
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from dateutil import parser
from dateutil.parser import ParserError
from pymongo import ASCENDING, DESCENDING

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
    bind_start_date = search_queries['bind_start_date']
    bind_end_date = search_queries['bind_end_date']
    print(bind_start_date,bind_end_date,"date")

    filtered_data = []
    total_filter = []
    total_data = []
    start_index = (page - 1) * items_per_page
    
    startdate_obj = datetime.strptime(bind_start_date, "%Y-%m-%dT%H:%M")
    enddate_obj = datetime.strptime(bind_end_date, "%Y-%m-%dT%H:%M")

    total_data = list(collection.find({'msisdn':input_value, 'time':{'$gte': datetime.combine(startdate_obj, datetime.min.time()),'$lte': datetime.combine(enddate_obj, datetime.max.time())}}, {'_id': 0}))
    
    print(startdate_obj,enddate_obj,"startenddate")
    
    # Applying filters based on selected checkboxes
    filters = []
    for key, values in selected_checkboxes.items():
        filters.append({key: {"$in": [str(value) for value in values]}})

    if filters:
        filter_query = {"$and": filters}  
        total_filter = collection.count_documents({"$and": [{'msisdn': input_value, 'time':{'$gte': datetime.combine(startdate_obj, datetime.min.time()),'$lte': datetime.combine(enddate_obj, datetime.max.time())}}, filter_query]})
        filtered_data = list(collection.find({"$and": [{'msisdn': input_value, 'time':{'$gte': datetime.combine(startdate_obj, datetime.min.time()),'$lte': datetime.combine(enddate_obj, datetime.max.time())}}, filter_query]}, {'_id': 0}).sort('_id').skip(start_index).limit(items_per_page))
    else:
        total_filter = collection.count_documents({'msisdn': input_value, 'time':{'$gte': datetime.combine(startdate_obj, datetime.min.time()),'$lte': datetime.combine(enddate_obj, datetime.max.time())}})
        filtered_data = list(collection.find({'msisdn': input_value, 'time':{'$gte': datetime.combine(startdate_obj, datetime.min.time()),'$lte': datetime.combine(enddate_obj, datetime.max.time())}}, {'_id': 0}).sort('_id').skip(start_index).limit(items_per_page))
    
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
    
    # filtered_data = list(collection.find({input_field_name:input_value}, {'_id': 0}).sort('_id').skip(start_index).limit(items_per_page))
    
    return jsonify({"data": filtered_data,"total": total_filter,"unique_values":unique_values})

if __name__ == '__main__':
    app.run(debug=True)

