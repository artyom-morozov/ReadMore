
import os
import csv
import sys
import re

from surprise import Dataset
from surprise import Reader

from collections import defaultdict


import numpy as np


class test:
    booksPath = '../datasets/books6ml.csv'
    ratingsPath = '../datasets/ratings6ml.csv'

    def loadDataSet(self):

        # Look for files relative to the directory we are running from

        ratingsDataset = 0
        self.bookID_to_name = {}
        self.name_to_bookID = {}

        reader = Reader(line_format='user item rating ', sep=',', rating_scale=(1,10) ,skip_lines=1)

        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader=reader)

        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
                bookReader = csv.reader(csvfile)
                next(bookReader)  #Skip header line
                for i, row in enumerate(bookReader):
                    bookID = int(row[0])
                    bookName = row[10]
                    self.bookID_to_name[bookID] = bookName
                    self.name_to_bookID[bookName] = bookID

        return ratingsDataset
    def getBookName(self, bookID):
        if bookID in self.bookID_to_name:
            return self.bookID_to_name[bookID]
        else:
            return ""
        
    def getBookID(self, bookName):
        if bookName in self.name_to_bookID:
            return self.name_to_bookID[bookName]
        else:
            return 0

    def getUserRatings(self, user):
        userRatings = []
        hitUser = False
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                userID = int(row[0])
                if (user == userID):
                    bookID = int(row[1])
                    rating = float(row[2])
                    userRatings.append((bookID, rating))
                    hitUser = True
                if (hitUser and (user != userID)):
                    break

        return userRatings
        # choose user with who liked those books
    def getBestMatch(self):
        my_fav_books = [357,7068, 13,840]
        hitUsers = []
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                bookID = int(row[1])
                rating = float(row[2])
                if (bookID in my_fav_books) and (rating == 4.0) :
                    userID = int(row[0])
                    if userID not in hitUsers:
                        hitUsers.append(userID)
                if len(hitUsers) == 35:
                    break

        return hitUsers

bk = test()

bk.loadDataSet()
bestUsers = bk.getBestMatch()

for user in bestUsers:
    ratings = bk.getUserRatings(user)
    print('Top 10 ratings for user ',user)
    count = 0
    for bookId, rating in sorted(ratings, key=lambda tup: tup[1], reverse=True):
        print(bk.getBookName(bookId),' - ',rating)
        count += 1
        if count == 7:
            break
    print('------------------------------------------------------')

