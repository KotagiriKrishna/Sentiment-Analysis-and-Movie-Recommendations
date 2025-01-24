from flask import Flask, request, jsonify,render_template,url_for,redirect
import pymysql

import pickle
import requests
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__,template_folder='templates',static_folder='static')


#signin pages
@app.route('/')
def index():

    return render_template('login.html')




#recommendations pages
@app.route('/recommendations')
def recommendations():
    return render_template('index.html')



#function to recommend top 5 similar movies

similarity = pickle.load(open("pickle_files/similarity.pkl","rb"))
movies_list = pickle.load(open('pickle_files/movies.pkl','rb'))
tfidf = pickle.load(open("pickle_files/Tfidfvec.pkl","rb"))
model = pickle.load(open("pickle_files/reviews_classifier.pkl","rb"))


movies = movies_list["title"].values

#function to find index of input movie
def movies_index(movie):
    for i in range(len(movies)):
        if movies_list["title"][i] == movie:
            return i

#function to recommend movies        
def recommend(movie):
    movie_index = movies_index(movie)
    distances = similarity[movie_index]
    similar_movies_list =  sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]  #using enum for holding the original indexes
    
    
    return similar_movies_list



@app.route('/recommend_movie', methods=['POST'])
def movie_recommend():
    data = request.get_json()
    user_text = data['text']
    
    recommended_list =[]
   
    similar_movies_list = recommend(user_text)
    for i in similar_movies_list:
        recommended_list.append(movies_list.iloc[i[0]].title)

    movie_list = {"result":
                  {"movies":recommended_list}}
   
    return jsonify(movie_list)

@app.route("/getsentiment",methods =['POST'])
def get_sentiment():
    data = request.get_json()
    review = data['text']
    sentence = tfidf.transform([review]).toarray()
    result = model.predict(sentence)[0]
    
    #☹️😊👎👍
    sentiment = ""
    if result:
        sentiment = "your review is  : Positive 👍"
    else:
        sentiment = "your review is  : Negative 👎"

    res_dict ={"result":
               {"sentiment":sentiment}}
    
    return jsonify(res_dict)



# MySQL configurations
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'CUSTOMERS'

# Create MySQL connection
db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)



# Create users table
def create_users_table():
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
            db.commit()
    except Exception as e:
        print("Error creating table:", e)

# Signup endpoint
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql, (username, password))
            db.commit()
        return jsonify({'message': 'Signup successful','redirect_url':'/recommendations'}), 200#redirect(url_for('portrfolio'))
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error signing up'}), 500

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            if result:
                return jsonify({'message': 'Signup successful','redirect_url':'/recommendations'}), 200
            else:
                return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error logging in'}), 500
    





if __name__ == '__main__':


    # Movies table to store user viewed movies for recommendations
    with db.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_movies (
                    Movies_id JSON  NOT NULL,
                    Movies_name JSON  NOT NULL,
                    Date DATE  NOT NULL,
                    id INT  NOT NULL,FOREIGN KEY (id) REFERENCES users(id)
                )
            """)
            db.commit()

   
    app.run(debug=True)

