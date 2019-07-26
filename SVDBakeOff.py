# -*- coding: utf-8 -*-
"""
Created on Thu May  3 11:11:13 2018

@author: Frank
"""

from BookCrossing import BookCrossing
from surprise import SVD, SVDpp
from surprise import NormalPredictor
from Evaluator import Evaluator

import random
import numpy as np

def LoadBookCrossingData():
    ml = BookCrossing()
    print("Loading movie ratings...")
    data = ml.loadBookCrossingLatestSmall()
    print("\nComputing movie popularity ranks so we can measure novelty later...")
    rankings = ml.getPopularityRanks()
    return (ml, data, rankings)

np.random.seed(0)
random.seed(0)

# Load up common data set for the recommender algorithms
(ml, evaluationData, rankings) = LoadBookCrossingData()

# Construct an Evaluator to, you know, evaluate them
evaluator = Evaluator(evaluationData, rankings)

# SVD
SVD = SVD()
evaluator.AddAlgorithm(SVD, "SVD")

# SVD++
SVDPlusPlus = SVDpp()
evaluator.AddAlgorithm(SVDPlusPlus, "SVD++")

# Just make random recommendations
Random = NormalPredictor()
evaluator.AddAlgorithm(Random, "Random")

# Fight!
evaluator.Evaluate(False)

evaluator.SampleTopNRecs(ml)
