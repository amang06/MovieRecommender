import streamlit as st
import pickle
import pandas as pd
import requests
from zipfile import ZipFile


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster_link(movie_id))
    return recommended_movies, recommended_movies_posters


def fetch_poster_link(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=fdf9674a0f5121a95c521d21c48085a6&language=en-US".format(
        movie_id)
    response = requests.get(url).json()
    path = "https://image.tmdb.org/t/p/w500" + response['poster_path']
    return path


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
with ZipFile("similarity.zip", 'r') as zObject:
    zObject.extractall(path='')

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button("Submit"):
    st.write("Selected movie name - ", selected_movie_name)
    recommendations, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(recommendations[0])
        st.image(posters[0])
    with col2:
        st.write(recommendations[1])
        st.image(posters[1])
    with col3:
        st.write(recommendations[2])
        st.image(posters[2])
    with col4:
        st.write(recommendations[3])
        st.image(posters[3])
    with col5:
        st.write(recommendations[4])
        st.image(posters[4])
