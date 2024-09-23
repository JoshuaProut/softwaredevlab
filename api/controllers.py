from flask import Blueprint, jsonify, request
from datetime import datetime
import db


items = Blueprint("items", __name__)
inventory = Blueprint("inventory", __name__)



@items.route("/", methods=['POST'])
def post_items():
    request_data = request.get_json()
    request_data["createdDate"] = datetime.now()

    #Lookup if item already exists
    found_item = db.mongo.db.schema.find_one({"name": request_data["name"]})
    if found_item:
        print("found item")
        
        # Determine and set new quantity
        filter_query = {"name" : request_data["name"]}
        new_quantity = found_item["quantity"] + request_data["quantity"]
        new_values = {"$set":{"quantity": new_quantity}}
        
        db.mongo.db.schema.update_one(filter_query, new_values)

    db.mongo.db.schema.insert_one(request_data)
    print (request_data)
    del request_data['_id']
    return jsonify(request_data)



@inventory.route("/", methods=['GET'])
def get_inventory():
    # Return the list of items
    # Return the item name and total quantity
    return jsonify(list(db.mongo.db.schema.find({}, {"_id": False})))

