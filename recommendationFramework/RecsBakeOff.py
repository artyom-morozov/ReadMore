# -*- coding: utf-8 -*-
"""
Created on Thu May  3 11:11:13 2018

@author: Frank
"""

from BookCrossing import BookCrossing
from surprise import SVD
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
    return (data, rankings)

np.random.seed(0)
random.seed(0)

# Load up common data set for the recommender algorithms
(evaluationData, rankings) = LoadBookCrossingData()

# Construct an Evaluator to, you know, evaluate them
evaluator = Evaluator(evaluationData, rankings)

# Throw in an SVD recommender
SVDAlgorithm = SVD(random_state=10)
evaluator.AddAlgorithm(SVDAlgorithm, "SVD")

# Just make random recommendations
Random = NormalPredictor()
evaluator.AddAlgorithm(Random, "Random")


# Fight!
evaluator.Evaluate(True)
