from flask import Blueprint
main = Blueprint('main', __name__)
import os
import json
from recommendationFramework import Engine

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, request

def create_app():
    global recommendation_engine 
    
    cur_dir = os.getcwd()


    
    books_path = os.path.join(cur_dir, 'datasets', 'books6ml.csv')
    ratings_path = os.path.join(cur_dir, 'datasets', 'ratings6ml.csv')
    model_path = os.path.join(cur_dir, 'models', 'ALS')

    recommendation_engine =  Engine.RecommendationEngine(ratings_path, books_path, model_path, 'ALS')    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app


@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings = recommendation_engine.alsTopNForUser(user_id,count)
    return json.dumps(top_ratings)
 
#  add this when adding recommendation for a book
# @main.route("/<int:user_id>/ratings/<int:book_id>", methods=["GET"])
# def book_ratings(user_id, book_id):
#     logger.debug("User %s rating requested for book %s", user_id, book_id)
#     ratings =  recommendation_engine.get_ratings_for_book_ids(user_id, [book_id])
#     return json.dumps(ratings)
 
 
@main.route("/<int:user_id>/ratings", methods = ["POST"])
def add_ratingsALS(user_id):
    # get the ratings from the Flask POST request object
    ratings_list = request.form.keys()[0].strip().split("\n")
    ratings_list = map(lambda x: x.split(","), ratings_list)
    # create a list with the format required by the engine (user_id, book_id, rating)
    ratings = map(lambda x: (user_id, int(x[0]), float(x[1])), ratings_list)
    # add them to the model using then engine API
    recommendation_engine.add_ratingsALS(ratings)

    return json.dumps(ratings)


 
 
