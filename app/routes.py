# ~/inventory_service/app/routes.py
from flask import Blueprint, jsonify, request, current_app # Import current_app for logger access
# from . import mysql # REMOVE THIS LINE - we are using db_manager
from app.models import db_manager # Keep this line

# Define your blueprint here. Give it a distinct name.
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/') # Use the blueprint object for routing
def home():
    return "Welcome to the Inventory Service! Use /items to manage inventory."

@main_blueprint.route('/test_db') # Use the blueprint object for routing
def test_db():
    try:
        # Use db_manager to execute a simple query
        # db_manager.execute_query returns None on error, or results/rowcount on success
        result = db_manager.execute_query("SELECT 1 AS test_column")
        if result is not None:
            return jsonify({"message": "Database connection successful!", "result": result})
        else:
            # If result is None, it means db_manager caught an error
            return jsonify({"message": "Database connection failed (check server logs for details)"}), 500
    except Exception as e:
        # This catch block is mostly for unexpected errors not handled by db_manager
        current_app.logger.error(f"An unexpected error occurred during database test: {e}")
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500

# --- CRUD Operations for Items ---

# GET all items and POST to create a new item
@main_blueprint.route('/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        query = "SELECT id, name, description, quantity, price FROM items"
        items = db_manager.execute_query(query)
        if items is not None:
            return jsonify(items), 200
        else:
            return jsonify({"error": "Failed to retrieve items"}), 500

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        name = data.get('name')
        description = data.get('description')
        quantity = data.get('quantity')
        price = data.get('price')

        if not name or quantity is None or price is None:
            return jsonify({"error": "Missing required fields: name, quantity, price"}), 400

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity < 0 or price < 0:
                return jsonify({"error": "Quantity and price cannot be negative"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Quantity must be an integer and price must be a float"}), 400

        query = "INSERT INTO items (name, description, quantity, price) VALUES (%s, %s, %s, %s)"
        params = (name, description, quantity, price)
        item_id = db_manager.execute_query(query, params)

        if item_id is not None:
            # Fetch the newly created item to return full details
            new_item_query = "SELECT id, name, description, quantity, price FROM items WHERE id = %s"
            new_item = db_manager.execute_query(new_item_query, (item_id,))
            if new_item:
                return jsonify(new_item[0]), 201 # Return the first (and only) item
            else:
                return jsonify({"message": "Item created but failed to retrieve details."}), 201
        else:
            return jsonify({"error": "Failed to create item"}), 500

# GET, PUT, DELETE a specific item by ID
@main_blueprint.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_item(item_id):
    if request.method == 'GET':
        query = "SELECT id, name, description, quantity, price FROM items WHERE id = %s"
        item = db_manager.execute_query(query, (item_id,))
        if item:
            return jsonify(item[0]), 200 # Return the first (and only) item
        else:
            return jsonify({"message": "Item not found"}), 404

    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # Allow partial updates: Only update fields that are provided
        updates = []
        params = []
        if 'name' in data:
            updates.append("name = %s")
            params.append(data['name'])
        if 'description' in data:
            updates.append("description = %s")
            params.append(data['description'])
        if 'quantity' in data:
            try:
                quantity = int(data['quantity'])
                if quantity < 0:
                    return jsonify({"error": "Quantity cannot be negative"}), 400
                updates.append("quantity = %s")
                params.append(quantity)
            except (ValueError, TypeError):
                return jsonify({"error": "Quantity must be an integer"}), 400
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    return jsonify({"error": "Price cannot be negative"}), 400
                updates.append("price = %s")
                params.append(price)
            except (ValueError, TypeError):
                return jsonify({"error": "Price must be a float"}), 400

        if not updates:
            return jsonify({"message": "No fields to update provided"}), 400

        query = "UPDATE items SET " + ", ".join(updates) + " WHERE id = %s"
        params.append(item_id)
        rows_affected = db_manager.execute_query(query, tuple(params))

        if rows_affected is not None and rows_affected > 0:
            # Fetch the updated item to return full details
            updated_item_query = "SELECT id, name, description, quantity, price FROM items WHERE id = %s"
            updated_item = db_manager.execute_query(updated_item_query, (item_id,))
            if updated_item:
                return jsonify(updated_item[0]), 200
            else:
                return jsonify({"message": "Item updated but failed to retrieve details."}), 200
        elif rows_affected == 0:
            return jsonify({"message": "Item not found or no changes made"}), 404
        else:
            return jsonify({"error": "Failed to update item"}), 500

    elif request.method == 'DELETE':
        query = "DELETE FROM items WHERE id = %s"
        rows_affected = db_manager.execute_query(query, (item_id,))

        if rows_affected is not None and rows_affected > 0:
            return jsonify({"message": "Item deleted successfully"}), 200
        elif rows_affected == 0:
            return jsonify({"message": "Item not found"}), 404
        else:
            return jsonify({"error": "Failed to delete item"}), 500
