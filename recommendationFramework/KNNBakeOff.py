# -*- coding: utf-8 -*-
"""
Created on Thu May  3 11:11:13 2018

@author: Frank
"""

from BookCrossing import BookCrossing
from surprise import KNNBasic
from surprise import NormalPredictor
from Evaluator import Evaluator

import random
import numpy as np

def LoadBookCrossingData():
    bk = BookCrossing()
    print("Loading book ratings...")
    data = bk.loadBookCrossingLatestSmall()
    print("\nComputing book popularity ranks so we can measure novelty later...")
    rankings = bk.getPopularityRanks()
    return (bk, data, rankings)

np.random.seed(0)
random.seed(0)

# Load up common data set for the recommender algorithms
(bk, evaluationData, rankings) = LoadBookCrossingData()

# Construct an Evaluator to, you know, evaluate them
evaluator = Evaluator(evaluationData, rankings)

# User-based KNN
UserKNN = KNNBasic(sim_options = {'name': 'cosine', 'user_based': True})
evaluator.AddAlgorithm(UserKNN, "User KNN")

# Item-based KNN
ItemKNN = KNNBasic(sim_options = {'name': 'cosine', 'user_based': False})
evaluator.AddAlgorithm(ItemKNN, "Item KNN")

# Just make random recommendations
Random = NormalPredictor()
evaluator.AddAlgorithm(Random, "Random")

# Fight!
evaluator.Evaluate(False)

evaluator.SampleTopNRecs(bk)
