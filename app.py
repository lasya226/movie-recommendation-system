from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ---------------------------
# LOAD DATASET
# ---------------------------
movies = pd.read_csv("static/dataset/movies.csv")
ratings = pd.read_csv("static/dataset/ratings.csv")

# Merge datasets
data = pd.merge(ratings, movies, on="movieId")

# Create user-item matrix
user_movie_matrix = data.pivot_table(
    index="userId",
    columns="title",
    values="rating"
).fillna(0)

movie_titles = list(user_movie_matrix.columns)

# SVD
SVD_model = TruncatedSVD(n_components=20)
matrix = SVD_model.fit_transform(user_movie_matrix)

# Similarity matrix
similarity_matrix = cosine_similarity(matrix)

# Recommendation function
def recommend_movies(movie_title):
    index = movie_titles.index(movie_title)
    similarity_scores = list(enumerate(similarity_matrix[index]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    top_movies = sorted_scores[1:11]
    recommendations = [movie_titles[i] for i, score in top_movies]
    return recommendations


# ---------------------------
# FRONTEND ROUTES
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html", movies=movie_titles)


@app.route("/recommend", methods=["POST"])
def recommend():
    movie_name = request.form["movie"]
    recs = recommend_movies(movie_name)
    return jsonify(recs)


# ---------------------------
# RUN FLASK APP
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)