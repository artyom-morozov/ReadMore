'''
As BookCrossing dataset is really sparce, this script will handle all inconsistencies in the data.
Run this script before working with the recommendation system.

'''

#necesarry imports
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import correlation
from sklearn.metrics.pairwise import pairwise_distances
import ipywidgets as widgets
from IPython.display import display, clear_output
from contextlib import contextmanager
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import os, sys
import re
import seaborn as sns

global metric,k
k=10
metric='cosine'

#Loading data
books = pd.read_csv('./datasets/books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
users = pd.read_csv('./datasets/users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('./datasets/ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
ratings.columns = ['userID', 'ISBN', 'bookRating']


#fixing the rows having 'DK Publishing Inc' as yearOfPublication

#ISBN '0789466953'
books.loc[books.ISBN == '0789466953','yearOfPublication'] = 2000
books.loc[books.ISBN == '0789466953','bookAuthor'] = "James Buckley"
books.loc[books.ISBN == '0789466953','publisher'] = "DK Publishing Inc"
books.loc[books.ISBN == '0789466953','bookTitle'] = "DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)"

#ISBN '078946697X'
books.loc[books.ISBN == '078946697X','yearOfPublication'] = 2000
books.loc[books.ISBN == '078946697X','bookAuthor'] = "Michael Teitelbaum"
books.loc[books.ISBN == '078946697X','publisher'] = "DK Publishing Inc"
books.loc[books.ISBN == '078946697X','bookTitle'] = "DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)"

#fixing the rows having 'Gallimard' as yearOfPublication

books.loc[books.ISBN == '2070426769','yearOfPublication'] = 2003
books.loc[books.ISBN == '2070426769','bookAuthor'] = "Jean-Marie Gustave Le ClÃ?Â©zio"
books.loc[books.ISBN == '2070426769','publisher'] = "Gallimard"
books.loc[books.ISBN == '2070426769','bookTitle'] = "Peuple du ciel, suivi de 'Les Bergers"

#Correcting the dtypes of yearOfPublication
books.yearOfPublication=pd.to_numeric(books.yearOfPublication, errors='coerce')

# Since the dataset was created in 2004 we assume that all values larger 2006 (2 year margin for breathability) are invalid  
#setting invalid years as NaN
books.loc[(books.yearOfPublication > 2006) | (books.yearOfPublication == 0),'yearOfPublication'] = np.NAN

#replacing NaNs with mean value of yearOfPublication
books.yearOfPublication.fillna(round(books.yearOfPublication.mean()), inplace=True)

#resetting the dtype as int32
books.yearOfPublication = books.yearOfPublication.astype(np.int32)

#replacing NaN publishers with 'other
books.loc[(books.ISBN == '193169656X'),'publisher'] = 'other'
books.loc[(books.ISBN == '1931696993'),'publisher'] = 'other'

#fixing incorrect age values
users.loc[(users.Age > 90) | (users.Age < 5), 'Age'] = np.nan

#replacing NaNs with mean
users.Age = users.Age.fillna(users.Age.mean())


#setting the data type as int
users.Age = users.Age.astype(np.int32)

#removing books that are not in the books dataset
ratings_new = ratings[ratings.ISBN.isin(books.ISBN)]

#As we are only interested in explict ratings we segregate them from the datasets
ratings_explicit = ratings_new[ratings_new.bookRating != 0]

limit = 20

#To cope up with computing power I have and to reduce the dataset size, I am considering users who have rated atleast 50 books
#and books which have atleast 20 ratings
counts1 = ratings_explicit['userID'].value_counts()
ratings_explicit = ratings_explicit[ratings_explicit['userID'].isin(counts1[counts1 >= limit].index)]
counts = ratings_explicit['bookRating'].value_counts()
ratings_explicit = ratings_explicit[ratings_explicit['bookRating'].isin(counts[counts >= limit].index)]

#drop random books
import pandas as pd
import numpy as np
np.random.seed(10)




#This function finds k similar items given the item_id and ratings matrix

def findksimilaritems(item_id, ratings, metric=metric, k=k):
    similarities=[]
    indices=[]
    ratings=ratings.T
    loc = ratings.index.get_loc(item_id)
    model_knn = NearestNeighbors(metric = metric, algorithm = 'brute')
    model_knn.fit(ratings)
    
    distances, indices = model_knn.kneighbors(ratings.iloc[loc, :].values.reshape(1, -1), n_neighbors = k+1)
    similarities = 1-distances.flatten()

    return similarities,indices
#This function predicts the rating for specified user-item combination based on item-based approach
def predict_itembased(user_id, item_id, ratings, metric = metric, k=k):
    prediction= wtd_sum =0
    user_loc = ratings.index.get_loc(user_id)
    item_loc = ratings.columns.get_loc(item_id)
    similarities, indices=findksimilaritems(item_id, ratings) #similar users based on correlation coefficients
    sum_wt = np.sum(similarities)-1
    product=1
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] == item_loc:
            continue
        else:
            product = ratings.iloc[user_loc,indices.flatten()[i]] * (similarities[i])
            wtd_sum = wtd_sum + product                              
    prediction = int(round(wtd_sum/sum_wt))
    
    #in case of very sparse datasets, using correlation metric for collaborative based approach may give negative ratings
    #which are handled here as below //code has been validated without the code snippet below, below snippet is to avoid negative
    #predictions which might arise in case of very sparse datasets when using correlation metric
    if prediction <= 0:
        prediction = 1   
    elif prediction >10:
        prediction = 10

    print('\nPredicted rating for user {0} -> item {1}: {2}'.format(user_id,item_id,prediction))   
    
    return prediction
    #This function utilizes above functions to recommend items for item/user based approach and cosine/correlation. 
#Recommendations are made if the predicted rating for an item is >= to 6,and the items have not been rated already
def recommendItem(user_id, ratings, metric=metric):    
    if (user_id not in ratings.index.values) or type(user_id) is not int:
        print( "User id should be a valid integer from this list :\n\n {} ".format(re.sub('[\[\]]', '', np.array_str(ratings_matrix.index.values))))
    else:    
        ids = ['Item-based (correlation)','Item-based (cosine)','User-based (correlation)','User-based (cosine)']
        select = widgets.Dropdown(options=ids, value=ids[0],description='Select approach', width='1000px')
        def on_change(change):
            clear_output(wait=True)
            prediction = []            
            if change['type'] == 'change' and change['name'] == 'value':            
                if (select.value == 'Item-based (correlation)') | (select.value == 'User-based (correlation)') :
                    metric = 'correlation'
                else:                       
                    metric = 'cosine'   
                with suppress_stdout():
                    if (select.value == 'Item-based (correlation)') | (select.value == 'Item-based (cosine)'):
                        for i in range(ratings.shape[1]):
                            if (ratings[str(ratings.columns[i])][user_id] !=0): #not rated already
                                prediction.append(predict_itembased(user_id, str(ratings.columns[i]) ,ratings, metric))
                            else:                    
                                prediction.append(-1) #for already rated items
                    else:
                        for i in range(ratings.shape[1]):
                            if (ratings[str(ratings.columns[i])][user_id] !=0): #not rated already
                                prediction.append(predict_userbased(user_id, str(ratings.columns[i]) ,ratings, metric))
                            else:                    
                                prediction.append(-1) #for already rated items
                prediction = pd.Series(prediction)
                prediction = prediction.sort_values(ascending=False)
                recommended = prediction[:10]
                print( "As per {0} approach....Following books are recommended...".format(select.value))
                for i in range(len(recommended)):
                     #print(t"{}. {}".format(i+1, books.bookTitle[recommended.index[i]].encode('utf-8')))   
                     print(i, ' ', books.bookTitle[recommended.index[i]].encode('utf-8'))                     
        select.observe(on_change)
        display(select)



# ratings_matrix = ratings_explicit.pivot(index='userID', columns='ISBN', values='bookRating')
# userID = ratings_matrix.index
# ISBN = ratings_matrix.columns
# #since NaNs cannot be handled by training algorithms, replacing these by 0, which indicates absence of ratings
# #setting data type
# ratings_matrix.fillna(0, inplace = True)
# ratings_matrix = ratings_matrix.astype(np.int32)
# recommendItem(74286, ratings_matrix)


#segregating explicit users
books_new = books[books.ISBN.isin(ratings_explicit.ISBN)]

# remove some books for efficiency
remove_n = 35000 + 52500 
drop_indices = np.random.choice(books_new.index, remove_n, replace=False)
books_new = books_new.drop(drop_indices)
ratings_explicit = ratings_explicit[ratings_explicit.ISBN.isin(books_new.ISBN)]
users_new = users[users.userID.isin(ratings_explicit.userID)]



#Now we can check final data shapes and save proccessed dataset
print('Checking user ages...')
print(sorted(users_new.Age.unique()))

print()

print('Checking if how many years of publication are null...')
books_new.yearOfPublication.isnull().sum()

print()

print('Explicit ratings shape:')
print(ratings_explicit.shape)
print(ratings_explicit.head())

print("number of users: " + str(users_new.shape[0]))
print("number of books: " + str(books_new.shape[0]))
print(ratings_explicit)
#save files
users_new.to_csv(r'X:\Программы\BookRecommender\Read.More\datasets\processed\users.csv', index = None, header=True)
books_new.to_csv(r'X:\Программы\BookRecommender\Read.More\datasets\processed\books.csv', index = None, header=True)
ratings_explicit.to_csv(r'X:\Программы\BookRecommender\Read.More\datasets\processed\ratings.csv', index = None, header=True)





