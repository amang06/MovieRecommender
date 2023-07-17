import streamlit as st
import pickle
import math
import pandas as pd
import requests
import datetime as dt
from datetime import datetime


def is_movie_in_range(release_date, start_date, end_date):
    return start_date < release_date.date() <= end_date


def recommend(movie, date1, date2):
    recommended_movies = []
    recommended_movies_posters = []

    # index of the provided movie
    movie_index = movies[movies['title'] == movie].index.item()

    # distance of provided movie with all movies
    distances = list(similarity[movie_index])
    movies_distance_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:]
    st.write(movies_distance_list)

    movies_in_range = movies.apply(
        lambda x: x if is_movie_in_range(x['release_date'], date1, date2) else None, axis=1)

    filtered_movies_in_range = list(movies_in_range.dropna())

    st.write(filtered_movies_in_range)

    for i in range(len(movies_distance_list)):
        for j in range(len(filtered_movies_in_range)):
            if movies_distance_list[i][0] == filtered_movies_in_range[j]['id']:
                recommended_movies.append(movies_in_range[i])
    st.write(recommended_movies)
    for i in range(len(recommended_movies)):
        recommended_movies_posters.append(fetch_poster_link(recommended_movies[i]['id']))
    return recommended_movies, recommended_movies_posters


def fetch_poster_link(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=fdf9674a0f5121a95c521d21c48085a6&language=en-US".format(
        movie_id)
    try:
        response = requests.get(url).json()
        path = "https://image.tmdb.org/t/p/w500" + response['poster_path']
    except:
        path = "https://softsmarttech.co.za/wp-content/uploads/2018/06/image-not-found-1038x576.jpg"
    return path


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies['release_date'] = pd.to_datetime(movies['release_date'])
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Which movie next?')
selected_movie_name = st.selectbox("Select a movie", movies['title'].values)
st.write('Release Date')
dcol1, dcol2 = st.columns(2)
with dcol1:
    d1 = st.date_input(
        "From",
        dt.date(2016, 1, 1))
with dcol2:
    d2 = st.date_input(
        "To",
        dt.date(datetime.today().year, datetime.today().month, datetime.today().day))

if st.button("Submit"):
    st.write("Selected movie name - ", selected_movie_name)
    if d2 < d1:
        st.write("End date should be bigger than from date")
    else:
        recommendations, posters = recommend(selected_movie_name, d1, d2)
        if len(recommendations) == 0:
            st.write('Unable to find recommendation within the provided date range!')
        else:
            col1, col2, col3, col4, col5 = st.tabs(['1', '2', '3', '4', '5'])
            with col1:
                st.write(recommendations[0].title)
                st.write('Release Date - ' + str(recommendations[0].release_date)[:-9])
                st.image(posters[0])
            with col2:
                st.write(recommendations[1].title)
                st.write('Release Date - ' + str(recommendations[1].release_date)[:-9])
                st.image(posters[1])
            with col3:
                st.write(recommendations[2].title)
                st.write('Release Date - ' + str(recommendations[2].release_date)[:-9])
                st.image(posters[2])
            with col4:
                st.write(recommendations[3].title)
                st.write('Release Date - ' + str(recommendations[3].release_date)[:-9])
                st.image(posters[3])
            with col5:
                st.write(recommendations[4].title)
                st.write('Release Date - ' + str(recommendations[4].release_date)[:-9])
                st.image(posters[4])
