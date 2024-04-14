from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import requests

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://adrianmendez01:nCNFvceq9BxCBTsa@cluster0.w3agl7j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["csulbdining"]
user_collection = db["user"]
review_collection = db["review"]


# Routes
@app.route('/')
def index():
    return "Welcome to your Flask-MongoDB app!"

"""@app.route('/review', methods=['POST'])
def add_review():
    # Get JSON data from request body
    data = request.get_json(force=True)

    # Check if all required fields are present
    required_fields = ['description', 'rating', 'dorm', 'menuitem', 'image', 'userid']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Insert the review data into the database
    inserted_id = review_collection.insert_one(data).inserted_id

    return jsonify({"message": "Review added successfully", "_id": str(inserted_id)})


@app.route('/review/<string:review_id>', methods=['PUT'])
def edit_review(review_id):
    # Get JSON data from request body
    data = request.get_json(force=True)

    # Check if all required fields are present
    required_fields = ['description', 'rating', 'dorm', 'menuitem', 'image', 'userid']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Find and update the review with the given review ID
    result = review_collection.update_one({"_id": ObjectId(review_id)}, {"$set": data})

    # Check if the review was found and updated
    if result.modified_count == 0:
        return jsonify({"error": "Review not found"}), 404

    return jsonify({"message": "Review updated successfully"})


# Route to calculate the average rating score for each dorm
@app.route('/reviewaverage')
def get_review_average():
    # Aggregation pipeline to calculate the average rating score for each dorm
    pipeline = [
        {
            "$group": {
                "_id": "$dorm",
                "average_rating": {"$avg": "$rating"}
            }
        }
    ]

    # Execute the aggregation pipeline
    result = list(review_collection.aggregate(pipeline))

    # Format the result into a single JSON object
    formatted_result = {}
    for item in result:
        formatted_result[item["_id"]] = item["average_rating"]

    return jsonify(formatted_result)


@app.route('/review/<string:review_id>', methods=['DELETE'])
def remove_review(review_id):
    # Check if the review ID is provided
    if not review_id:
        return jsonify({"error": "Review ID is missing"}), 400

    # Find and delete the review with the given review ID
    result = review_collection.delete_one({"_id": ObjectId(review_id)})

    # Check if the review was found and deleted
    if result.deleted_count == 0:
        return jsonify({"error": "Review not found"}), 404

    return jsonify({"message": "Review deleted successfully"})


@app.route('/searchimage', methods=['GET'])
def search_image():
    API_KEY = 'AIzaSyDRoDaxcvlZF-1v80GQ9vaJdzNwVbT6E6E'
    SEARCH_ENGINE_ID = 'c0ecba8d944aa4897'

    search_query = request.args.get('q', '')

    url = 'https://www.googleapis.com/customsearch/v1'

    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'searchType': 'image',
        'image_size': 'large'
    }

    response = requests.get(url, params=params)
    results = response.json()

    if 'items' in results:
        return jsonify({'image_url': results['items'][0]['link']})
    else:
        return jsonify({'error': 'No images found for the query'}), 404
"""

if __name__ == '__main__':
    app.run(debug=True)
