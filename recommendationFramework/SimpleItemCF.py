# -*- coding: utf-8 -*-


from BookCrossing import BookCrossing
from surprise import KNNBasic
import heapq
from collections import defaultdict
from operator import itemgetter
        
testSubject = '74286'
k = 10

bk = BookCrossing()
data = bk.loadBookCrossingLatestSmall()

trainSet = data.build_full_trainset()

sim_options = {'name': 'cosine',
               'user_based': False
               }

model = KNNBasic(sim_options=sim_options)
model.fit(trainSet)
simsMatrix = model.compute_similarities()

testUserInnerID = trainSet.to_inner_uid(testSubject)

# Get the top K items we rated
testUserRatings = trainSet.ur[testUserInnerID]
kNeighbors = heapq.nlargest(k, testUserRatings, key=lambda t: t[1])

# Get similar items to stuff we liked (weighted by rating)
candidates = defaultdict(float)
for itemID, rating in kNeighbors:
    similarityRow = simsMatrix[itemID]
    for innerID, score in enumerate(similarityRow):
        candidates[innerID] += score * (rating / 5.0)
    
# Build a dictionary of stuff the user has already seen
watched = {}
for itemID, rating in trainSet.ur[testUserInnerID]:
    watched[itemID] = 1
    
# Get top-rated items from similar users:
pos = 0
for itemID, ratingSum in sorted(candidates, key=lambda tup: tup[1], reverse=True):
    if not itemID in watched:
        bookID = trainSet.to_raw_iid(itemID)
        print(bk.getBookName(bookID), ratingSum)
        pos += 1
        if (pos > 10):
            break

    


