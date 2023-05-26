from PIL import Image
import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title="StreamFlix", page_icon=":tada:", layout="wide")
st.snow()

st.image("images/logo1.png")

# using lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_coding = load_lottieurl(
    "https://assets7.lottiefiles.com/private_files/lf30_F6EtR7.json")



# using css styles for the contact form
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("styles/styles.css")


# fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=5cc4c3a5db0dca7558751e1eb0ef804e'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]

    recommended_movies = []
    recommended_movies_posters = []
    synopsis = []
    genres = []
    ratings = []
    actors = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch actors
        actors.append(movies.iloc[i[0]].cast)
        # fetch ratings
        ratings.append(movies.iloc[i[0]].ratings)
        # fetch genres
        genres.append(movies.iloc[i[0]].genres)
        # fetch synopsis
        synopsis.append(movies.iloc[i[0]].synopsis)
        # fetch poster by API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters, synopsis, genres, ratings, actors


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox('Enter any movie name',
                              movies['title'].values)


if st.button('Recommend'):
    names, posters, desc, genre, rating, cast = recommend(selected_movie)

    dupeCast = [[] for i in range(8)]

    st.write("---")
    st.header("Recommended Movies for you")
    st.write("##")

    for i in range(8):

        for actor in cast[i]:
            for m in range(len(actor) - 1, -1, -1):
                if actor[m].isupper():
                    dupeCast[i].append(actor[:m] + " " + actor[m:])
                    break

        image_column, text_column = st.columns((1, 2))
        with st.container():
            with image_column:
                st.image(posters[i])

            with text_column:
                st.subheader(names[i])
                st.write("##")
                st.write('Ratings: ', rating[i], '⭐')
                st.write('Genres: ', ", ".join(genre[i]))
                st.write('Cast: ', ", ".join(dupeCast[i]))
                st.write('Synopsis: ')
                st.caption(desc[i])
