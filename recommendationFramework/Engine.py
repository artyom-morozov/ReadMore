from surprise import SVDpp
from recommendationFramework.EvaluationData import EvaluationData
from recommendationFramework.BookCrossing import BookCrossing
from pyspark.sql import Row
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS

import csv

# books_path = '../datasets/books6ml.csv'
# book_ratings_path = '../datasets/ratings6ml.csv'
# model_path = '../models/ALS'


class RecommendationEngine:

    def loadBookNames(self):
        print("Loading book names...")
        bookID_to_name = {}
        with open(self.books_path, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)  #Skip header line
            for row in bookReader:
                bookID = int(row[0])
                bookName = row[10]
                bookID_to_name[bookID] = bookName
        return bookID_to_name

    def loadDataFrame(self, ratings_path):
        print("Loading data frames...")
        lines = self.spark.read.option("header", "true").csv(ratings_path).rdd
        ratingsRDD = lines.map(lambda p: Row(userId=int(p[0]), bookId=int(p[1]),
                                                rating=(float(p[2])))) # scale to 10
        return self.spark.createDataFrame(ratingsRDD)

    def loadBookData(self):
        bk = BookCrossing()
        print("Loading book ratings...")
        data = bk.loadBookCrossingLatestSmall()
        print("\nComputing book popularity ranks so we can measure novelty later...")
        rankings = bk.getPopularityRanks()
        return (bk, data, rankings)
    
    def train_ALSmodel(self):
        """Train the ALS model with the current dataset
        """
        self.model = self.als.fit(self.ratings)
        self.model.write().overwrite().save(self.model_path)
    
    def __init__(self, dataset_path, books_path, model_path, algo='SVD'  ):
        """Init the recommendation engine given a Spark context and a dataset
        """
        self.ratings_path = dataset_path
        self.model_path = model_path
        self.books_path = books_path
        if algo == 'SVD':
            self.algo = algo
            self.SVD = SVDpp()
            (bk, data, rankings) = self.loadBookData()
            self.bk = bk
            self.rankings = rankings
            self.dataset = EvaluationData(data, rankings)

        # ALS algorithm part
        self.spark = SparkSession\
                    .builder\
                    .appName("ReadMore")\
                    .config("spark.executor.cores", '4')\
                    .getOrCreate()

        self.bookID_to_name = self.loadBookNames()
        self.als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="bookId", ratingCol="rating",
                    coldStartStrategy="drop")
        self.ratings = self.loadDataFrame(dataset_path)
        self.train_ALSmodel() 

        # # Load ratings data for later use
        # logger.info("Loading Ratings data...")
        # ratings_file_path = os.path.join(dataset_path, 'ratings.csv')
        # ratings_raw_RDD = self.sc.textFile(ratings_file_path)
        # ratings_raw_data_header = ratings_raw_RDD.take(1)[0]
        # self.ratings_RDD = ratings_raw_RDD.filter(lambda line: line!=ratings_raw_data_header)\
        #     .map(lambda line: line.split(",")).map(lambda tokens: (int(tokens[0]),int(tokens[1]),float(tokens[2]))).cache()
        # # Load movies data for later use
        # logger.info("Loading Movies data...")
        # movies_file_path = os.path.join(dataset_path, 'movies.csv')
        # movies_raw_RDD = self.sc.textFile(movies_file_path)
        # movies_raw_data_header = movies_raw_RDD.take(1)[0]
        # self.movies_RDD = movies_raw_RDD.filter(lambda line: line!=movies_raw_data_header)\
        #     .map(lambda line: line.split(",")).map(lambda tokens: (int(tokens[0]),tokens[1],tokens[2])).cache()
        # self.movies_titles_RDD = self.movies_RDD.map(lambda x: (int(x[0]),x[1])).cache()
        # # Pre-calculate movies ratings counts
        # self.__count_and_average_ratings()
 
        # # Train the model
        # self.rank = 8
        # self.seed = 5L
        # self.iterations = 10
        # self.regularization_parameter = 0.1
        

    def add_ratingsALS(self, ratings):
        """Add additional book ratings in the format (user_id, book_id, rating)
        """
        rows = []
        for rating in ratings:
            rows.append(Row(userId=int(rating[0]), bookId=int(rating[1]), rating=float(rating[2])))
        newFrame = self.spark.createDataFrame(rows)
        self.ratings = self.ratings.union(newFrame)

        # Re-train the ALS model with the new ratings
        self.train_ALSmodel()

        return ratings
    def showUser(self, userID):
        myUser = self.ratings.filter(self.ratings['userId'] == int(userID))
        print('Showing user')
        myUser.show()
    # Return top 10 book rating pairs for user
    def alsTopNForUser(self, userId, n=10):
        print("Generating top {} recommendations for user with id - {}...".format(n, userId))
        userDF = self.ratings.filter(self.ratings['userId'] == int(userId)).distinct().limit(1)
        print('Showing...')
        userDF.show()
        recommendationsDF = self.model.recommendForUserSubset(userDF, n).collect()
        recommendations = []
        for row in recommendationsDF:
            for rec in row.recommendations:
                if rec.bookId in self.bookID_to_name:
                    recommendations.append((rec.bookId, rec.rating))
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations


    # Generate top 10 recommendations for user with id
    def SampleTopNRecs(self, userId, n=10):
        print("\nBuilding recommendation model...")
        trainSet = self.dataset.GetFullTrainSet()
        self.SVD.fit(trainSet)
        
        print("Computing recommendations...")
        testSet = self.dataset.GetAntiTestSetForUser(userId)

        predictions = self.SVD.test(testSet)
        
        recommendations = []
        
        for userID, bookID, actualRating, estimatedRating, _ in predictions:
            recommendations.append((bookID, estimatedRating))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:n]

    def chooseSVD(self):
        self.algo = 'SVD'

    def chooseALS(self):
        self.algo = 'ALS'