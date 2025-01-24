# SENTIMENT ANALYSIS AND MOVIE RECOMMENDATIONS
I have used ML Algorithms for classification like Naive Bayes Random Forest, Decision Tree , SVM and
NLP for tokenization , stemming , TF-IDF , Count Vectorizer.

# DATASETS

DATASETS :- ( Download from KAGGLE ) and store it in folder (datasets/)

1.IMDB_reviews_Dataset.csv
2.tmdb_5000_credits.csv
3.tmdb_5000_movies.csv


# TO RUN

    To run use the following command

    ### install requirements 

       >>> pip install -r requirements.txt

    After installing kindly run all the notebook code then Pickle files will be saved then move them into 
    
             --->  pickles_folder  <---
             
    ### server.py  

       >>> python main.py        --> SIMPLE UI (if API not works)

       >>> python main_API.py    --> It uses TMDB API to fetch IMAGES AND REVIEWS from website  (***** RECOMMENDED *****)

# OUTPUT check in output folder
    I have used Tmdb API for fetching real time movie reviews for SENTIMENT ANALYSIS and  for Fetching movie posters.


    **********  Sometimes API does not work so in that case please consider output folder. **********



# This project is divided into 2 parts 

## 1 - Movie Recommendations :-

        In this we take movie name as input from the users and recommend them with the similar genre or relevant movies accordingly using "COSINE SIMILARITY".

        CODE :
            you can code related to movie recommendations in the python jupyter notebook - 
            
              ---------  ("movie_recommendation_model.ipynb")    ------


## 2 - Sentiment Analysis of Movie Reviews :-

        In this we take Review as an input and classify whether it is a positive or negative review

        CODE :
            you can code related to Sentiment Analysis in the python jupyter notebook -

                ---------  ("reviews_sentiment_analysis.ipynb")    ------




