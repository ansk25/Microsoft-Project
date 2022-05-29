import streamlit as st
import pickle
import pandas as pd
import requests
from altair.vegalite.v4.theme import theme

#page configuration
st.set_page_config(page_title="Movie Recommender System", page_icon=None, layout="centered",
                   initial_sidebar_state="auto", menu_items={'About' : "This website recommends the top 5 movies similar to the searched movie"})

#function to get poster image of movie
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                            '}?api_key=785d2da01a3cef30b131bc1b199eb5bb&language=en-US'.format(movie_id))
    data = response.json()      #converting to json
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

#function to get rating of movie
def fetch_rating(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                            '}?api_key=785d2da01a3cef30b131bc1b199eb5bb&language=en-US'.format(movie_id))
    data = response.json()      #converting to json
    return data['vote_average']

#function to get overview of movie
def fetch_overview(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                            '}?api_key=785d2da01a3cef30b131bc1b199eb5bb&language=en-US'.format(movie_id))
    data = response.json()      #converting to json
    return data['overview']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]    #calculating distance using cosine similarity
    #getting top 5 movies from sorted list
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    movies_posters = []
    movie_rating = []
    movie_overview = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch posters of the movies from API
        movies_posters.append(fetch_poster(movie_id))
        # fetch ratings of the movies from API
        movie_rating.append(fetch_rating(movie_id))
        # fetch overview of the movies from API
        movie_overview.append(fetch_overview(movie_id))


    return recommended_movies, movies_posters, movie_rating, movie_overview

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

option = st.selectbox('Recommendations of the movie:',
                       movies['title'].values)

if st.button('Recommend'):
    recommendations, posters, ratings, overview = recommend(option)
    for i in recommendations:
        st.write(i)

    col1, col2 = st.columns(2)

    with col1:
        #movie 1
        st.text(recommendations[0])
        st.image(posters[0])
        expander_overview = st.expander("See Overview")
        expander_overview.write(overview[0])
        expander_rating = st.expander("See Rating")
        expander_rating.write(ratings[0])

        # movie 3
        st.text(recommendations[2])
        st.image(posters[2])
        expander_overview = st.expander("See Overview")
        expander_overview.write(overview[2])
        expander_rating = st.expander("See Rating")
        expander_rating.write(ratings[2])

        # movie 5
        st.text(recommendations[4])
        st.image(posters[4])
        expander_overview = st.expander("See Overview")
        expander_overview.write(overview[4])
        expander_rating = st.expander("See Rating")
        expander_rating.write(ratings[4])

    with col2:
        # movie 2
        st.text(recommendations[1])
        st.image(posters[1])
        expander_overview = st.expander("See Overview")
        expander_overview.write(overview[1])
        expander_rating = st.expander("See Rating")
        expander_rating.write(ratings[1])

        # movie 4
        st.text(recommendations[3])
        st.image(posters[3])
        expander_overview = st.expander("See Overview")
        expander_overview.write(overview[3])
        expander_rating = st.expander("See Rating")
        expander_rating.write(ratings[3])










