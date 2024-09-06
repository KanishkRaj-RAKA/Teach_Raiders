from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Create a MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']

@app.route('/image', methods=['GET'])
def get_image():
    # Retrieve the image data from MongoDB
    image_data = collection.find_one({'_id': 'myimage'})['image']

    # Return the image data as a response
    return jsonify({'image': image_data})

if __name__ == '__main__':
    app.run(debug=True)