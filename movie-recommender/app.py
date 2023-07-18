import streamlit as st
import pickle
import pandas as pd
import requests
import datetime as dt
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def is_movie_in_range(release_date, start_date, end_date):
    return start_date < release_date.date() <= end_date


def recommend(movie, date1, date2):
    recommended_movies = []
    recommended_movies_posters = []

    # index of the provided movie
    given_movie_index = movies[movies['title'] == movie].index.item()

    movies['release_date'] = movies.apply(
        lambda x: x['release_date'] if is_movie_in_range(x['release_date'], date1, date2) else None, axis=1)
    movies_in_range = movies[movies['release_date'].notna()]

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies_in_range['tags']).toarray()

    cosine_similarity(vectors)
    similarity = cosine_similarity(vectors)
    silmilarmovies = sorted(list(enumerate(similarity[given_movie_index])), reverse=True, key=lambda x: x[1])[1:]

    for i in range(0, 5):
        recommended_movies.append(movies_in_range.iloc[silmilarmovies[i][0]])
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


movies_dict = pickle.load(open('movie-recommender/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movies['release_date'] = pd.to_datetime(movies['release_date'])

st.title('Which movie next?')
selected_movie_name = st.selectbox("Select a movie you like", movies['title'].values)
st.write('Release Date')
dcol1, dcol2 = st.columns(2)
with dcol1:
    d1 = st.date_input(
        "From",
        dt.date(2016, 1, 1),
        min_value=dt.date(1950, 1, 1))
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
            col1, col2, col3, col4, col5 = st.tabs([recommendations[0].title, recommendations[1].title, recommendations[2].title, recommendations[3].title, recommendations[4].title])
            with col1:
                st.markdown("<h3 style='text-align: center'>" + recommendations[0].title + "</h3>",
                            unsafe_allow_html=True)
                st.markdown("<p style='text-align: center'>Release Date - " + str(recommendations[0].release_date)[
                                                                              :-9] + "</p>", unsafe_allow_html=True)
                st.image(posters[0], use_column_width="always")
            with col2:
                st.markdown("<h3 style='text-align: center'>" + recommendations[1].title + "</h3>",
                            unsafe_allow_html=True)
                st.markdown("<p style='text-align: center'>Release Date - " + str(recommendations[1].release_date)[
                                                                              :-9] + "</p>", unsafe_allow_html=True)
                st.image(posters[1], use_column_width="always")
            with col3:
                st.markdown("<h3 style='text-align: center'>" + recommendations[2].title + "</h3>",
                            unsafe_allow_html=True)
                st.markdown("<p style='text-align: center'>Release Date - " + str(recommendations[2].release_date)[
                                                                              :-9] + "</p>", unsafe_allow_html=True)
                st.image(posters[2], use_column_width="always")
            with col4:
                st.markdown("<h3 style='text-align: center'>" + recommendations[3].title + "</h3>",
                            unsafe_allow_html=True)
                st.markdown("<p style='text-align: center'>Release Date - " + str(recommendations[3].release_date)[
                                                                              :-9] + "</p>", unsafe_allow_html=True)
                st.image(posters[3], use_column_width="always")
            with col5:
                st.markdown("<h3 style='text-align: center'>" + recommendations[4].title + "</h3>",
                            unsafe_allow_html=True)
                st.markdown("<p style='text-align: center'>Release Date - " + str(recommendations[4].release_date)[
                                                                              :-9] + "</p>", unsafe_allow_html=True)
                st.image(posters[4], use_column_width="always")
