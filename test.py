import os
from recommendationFramework import Engine
import json
    
cur_dir = os.getcwd()



books_path = os.path.join(cur_dir, 'datasets', 'books6ml.csv')
ratings_path = os.path.join(cur_dir, 'datasets', 'ratings6ml.csv')
model_path = os.path.join(cur_dir, 'models', 'ALS')

recommendation_engine =  Engine.RecommendationEngine(ratings_path, books_path, model_path, 'ALS')    
recommendation_engine.add_ratingsALS([
     (3000001, 840, 5),
     (3000001, 7068, 5),
     (3000001, 7269, 4),
     (3000001, 8, 3),
 ])
recommendation_engine.showUser(3000001)
# top n for test user 
top_ratings = recommendation_engine.alsTopNForUser(3000001,10)

for i, rating in enumerate(top_ratings):
    name = recommendation_engine.bookID_to_name[rating[0]]
    print('{}. {} - *'.format(i+1, name, rating[1]))