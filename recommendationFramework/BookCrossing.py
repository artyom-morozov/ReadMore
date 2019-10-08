import os
import csv
import sys
import re

from surprise import Dataset
from surprise import Reader

from collections import defaultdict
import numpy as np

class BookCrossing:
    
    bookID_to_name = {}
    name_to_bookID = {}
    ratingsPath = './datasets/processed/ratings.csv'
    booksPath = './datasets/processed/books.csv'
    usersPath = './datasets/processed/users.csv'

    def loadBookCrossingLatestSmall(self):

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
                    bookID = row[0]
                    bookName = row[1]
                    self.bookID_to_name[bookID] = bookName
                    self.name_to_bookID[bookName] = bookID

        return ratingsDataset

    def getUserRatings(self, user):
        userRatings = []
        hitUser = False
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                userID = int(row[0])
                if (user == userID):
                    bookID = row[1]
                    rating = float(row[2])
                    userRatings.append((bookID, rating))
                    hitUser = True
                if (hitUser and (user != userID)):
                    break

        return userRatings

    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                bookID = row[1]
                ratings[bookID] += 1
        rank = 1
        for bookID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[bookID] = rank
            rank += 1
        return rankings

    def getYears(self):
        years = defaultdict(int)
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)
            for row in bookReader:
                bookID = row[0]
                year = int(row[3])
                years[bookID] = year
        return years
    
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



