import pickle
import re
import requests
import pandas as pd
from tmdbv3api import TMDb
import nltk
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

#function to recommend top 5 similar movies
similarity = pickle.load(open("pickle_files/similarity.pkl","rb"))
movies_list = pickle.load(open('pickle_files/movies.pkl','rb'))
tfidf = pickle.load(open("pickle_files/Tfidfvec.pkl","rb"))
model = pickle.load(open("pickle_files/reviews_classifier.pkl","rb"))

# function to get sentiment
def get_sentiment(review):
    #removing html tags <br /> 
    soup = BeautifulSoup(review,"html.parser")
    review =  soup.get_text()
    review = re.sub("[^a-zA-Z]"," ",review)
    #stemming
    stemmer =  PorterStemmer()
    stemmed_review = " ".join([stemmer.stem(word) for word in word_tokenize(review)])

    sentence = tfidf.transform([stemmed_review]).toarray()
    result = model.predict(sentence)[0]
    
    #☹️😊👎👍
    if result:
        return review,"👍"
    else:
        return review,"👎"
    
#fetching reviews and their sentiments    
def get_reviews(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}/reviews?api_key={}".format(movie_id,tmdb.api_key))
    reviews=response.json()
    sent_analysis=[]
    if reviews["total_results"]<10:
        for i in range(reviews["total_results"]):
            content=reviews["results"][i]["content"]
            review, sentiment = get_sentiment(content)
            sent_analysis.append({review:sentiment})
    else:
        for i in range(0,11):
            content=reviews["results"][i]["content"]
            review,sentiment = get_sentiment(content)
            sent_analysis.append({review:sentiment})        
    return sent_analysis

def movie_id_pred(movie):
    id1=movies_list.loc[movies_list["title"]==movie,'movie_id'].values
    cont=get_reviews(id1[0]) # function call to get reviews
    reviews=[]
    sentiment=[]
    for i in cont:
        for keys,values in i.items():
            reviews.append(keys)
            sentiment.append(values)
    return reviews,sentiment

#fetching posters  
tmdb=TMDb()
tmdb.api_key = "f73e1601b65f3bc2522fc83e4f0fd5ed"

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data = response.json()
    if "poster_path" in data or data["poster_path"] != None:
        return 'https://image.tmdb.org/t/p/w500/' +  data["poster_path"] 
    else:
        return " "

#function to recommend top similar movies
def movies_index(movie):
    for i in range(len(movies)):
        if movies_list["title"][i] == movie:
            return i

def recommend(movie):
    movie_index = movies_index(movie)
    distances = similarity[movie_index]
    similar_movies_list =  sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:21]  #using enum for holding the original indexes   
    recommended_movies = []
    recommended_movies_posters = []

    for i in similar_movies_list:
        movie_id = movies_list.iloc[i[0]].movie_id
        poster_path = fetch_poster(movie_id)
        # checking whether the poster path is Available or not
        if poster_path != " ":
            recommended_movies.append(movies_list.iloc[i[0]].title)
            recommended_movies_posters.append(poster_path)
    #call movie_id_pred function to get the sentiment of the reviews
    reviews,sentiment = movie_id_pred(movie)
    return recommended_movies ,recommended_movies_posters , reviews , sentiment
                          
#loading movies list
movies = movies_list["title"].values

        
