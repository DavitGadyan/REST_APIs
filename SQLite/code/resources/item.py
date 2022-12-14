import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    # to parse and manage inputs in body
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left be blank!!"
                        )

    @jwt_required() 
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}, 404

    @classmethod
    def find_by_name(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with the name {} already exists!!".format(name)}, 400

        data = Item.parser.parse_args()
        # data = request.get_json()
        item = {"name": name, "price": data["price"]}

        try:
            self.insert(item)
        except:
            return {"message": "Internal server error has occured"}, 500

        return item, 201

    @classmethod
    def insert(self, item):

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}

        if item is None:
            self.insert(updated_item)
        else:
            self.update(updated_item)

        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()
        return {"message": "Item updated"}

class ItemList(Resource):

    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        item_df = result.fetchall()
        items = []
        for row in item_df:
            items.append({"name": row[0], "price": row[1]})

        connection.close()
        return {"items": items}, 200