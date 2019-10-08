# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row

import csv

books_path = '../datasets/books6ml.csv'
ratings_path = '../datasets/ratings6ml.csv'
model_path = '../models/ALS'
def loadBookNames():
    bookID_to_name = {}
    with open(books_path, newline='', encoding='ISO-8859-1') as csvfile:
        bookReader = csv.reader(csvfile)
        next(bookReader)  #Skip header line
        for row in bookReader:
            bookID = int(row[0])
            bookName = row[10]
            bookID_to_name[bookID] = bookName
    return bookID_to_name

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("ALSExample")\
        .config("spark.executor.cores", '4')\
        .getOrCreate()

    lines = spark.read.option("header", "true").csv(ratings_path).rdd

    ratingsRDD = lines.map(lambda p: Row(userId=int(p[0]), bookId=int(p[1]),
                                         rating=float(p[2])))
    
    ratings = spark.createDataFrame(ratingsRDD)
    
    (training, test) = ratings.randomSplit([0.8, 0.2])

    als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="bookId", ratingCol="rating",
              coldStartStrategy="drop")
    model = als.fit(training)

    predictions = model.transform(test)
    evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
                                    predictionCol="prediction")
    rmse = evaluator.evaluate(predictions)
    print("Root-mean-square error = " + str(rmse))

    userRecs = model.recommendForAllUsers(10)
    model.write().overwrite().save(model_path)
    favorite_user = userRecs.filter(userRecs['userId'] == 115).collect()
    
    spark.stop()

    bookID_to_name = loadBookNames()
        
    for row in favorite_user:
        for rec in row.recommendations:
            if rec.bookId in bookID_to_name:
                print(bookID_to_name[rec.bookId])

