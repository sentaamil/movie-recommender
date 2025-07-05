import pickle
import streamlit as st
import requests
import time

# ------------------- Function to Fetch Posters ------------------- #
def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ------------------- Recommendation Logic ------------------- #
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
    )
    names, posters = [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return names, posters

# ------------------- Page Setup ------------------- #
st.set_page_config(
    page_title="🎥 AI Movie Recommender",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------- Custom CSS Animation + Fonts ------------------- #
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Poppins:wght@400;700&display=swap');

    html, body, .stApp {
        background-color: #0f0f0f;
        color: #f5f5f5;
        font-family: 'Poppins', sans-serif;
    }

    h1 {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 3.5rem;
        animation: fadeIn 2s ease-in-out;
        color: #ff4c60;
        text-shadow: 2px 2px 5px rgba(255, 76, 96, 0.5);
    }

    .stButton > button {
        background: linear-gradient(135deg, #ff4c60, #ff6e7f);
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 76, 96, 0.3);
    }

    .stButton > button:hover {
        transform: scale(1.07);
        box-shadow: 0 6px 20px rgba(255, 76, 96, 0.5);
    }

    .movie-card {
        text-align: center;
        transition: transform 0.4s ease;
        padding: 10px;
    }

    .movie-card:hover {
        transform: scale(1.05);
    }

    .movie-title {
        font-size: 1.1rem;
        margin-top: 0.5em;
        color: #ffffff;
        font-weight: 600;
    }

    img {
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(255, 76, 96, 0.3);
    }

    @keyframes fadeIn {
        0% {opacity: 0; transform: translateY(-20px);}
        100% {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- Load Models ------------------- #
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# ------------------- Title ------------------- #
st.markdown("<h1>🎬 AI Movie Recommender</h1>", unsafe_allow_html=True)

# ------------------- Dropdown ------------------- #
selected_movie = st.selectbox("🔎 Search or select a movie you like:", movies['title'].values)

# ------------------- Recommend Button ------------------- #
if st.button('✨ Show Recommendations'):
    with st.spinner("Generating your movie experience... 🎞️"):
        time.sleep(1)
        names, posters = recommend(selected_movie)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.markdown(f"""
                    <div class="movie-card">
                        <img src="{posters[i]}" width="100%" />
                        <div class="movie-title">{names[i]}</div>
                    </div>
                """, unsafe_allow_html=True)
