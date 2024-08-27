#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response ,jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route("/restaurants", methods=['GET'])
def get_restaurants():
    restaurants =Restaurant.query.all()
    if restaurants:
        body =(restaurant.to_dict() for restaurant in restaurants)
        status =200
    else:
        body={'message':'Restaurant not found'} 
        status =400
    return make_response(body,status)
    

@app.route("/restaurant/<int:id>",methods=['GET'])
def get_restaurant_by_id(id):
    restaurant =Restaurant.query.filter(Restaurant.id ==id).first()
    if restaurant:
        body=restaurant.to_dict()
        status=200
    else:
        body={'message':f'Restaurant{id}not found'}
        status=404
    return make_response(body,status)
        

    

@app.route("/restaurant/<int:id>" ,methods =['DELETE'])
def del_restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()

    if request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Restaurant deleted."
        }

        response = make_response(
            response_body,
            200
        )
        return response

    

@app.route("/pizzas", methods=['GET'])
def get_pizzas():
    pizzas =Pizza.query.all()
    if pizzas:
        body =(pizza.to_dict() for pizza in pizzas)
        status =200
    else:
        body={'message':'Pizzas not found'} 
        status =400
    return make_response(body,status)
    
    

@app.route("/POST/restaurant_pizzas", methods =['POST'])
def post_restaurant_pizzas():
   
    if request.method == 'POST':
        new_restaurant_pizza=RestaurantPizza(
            price=request.get('price'),
            restaurant_id=request.get('restaurant_id'),
            pizza_id=request.get('pizza_id')
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        restaurant_pizza_dict=new_restaurant_pizza.to_dict()

        response = make_response(
            restaurant_pizza_dict,
            201
        )

        return response
    


if __name__ == "__main__":
    app.run(port=5555, debug=True)
