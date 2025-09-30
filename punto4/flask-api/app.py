from flask import Flask, jsonify, request
from neo4j import GraphDatabase
import os

app = Flask(__name__)

uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "secret")

driver = GraphDatabase.driver(uri, auth=(user, password))

@app.route('/users', methods=['GET'])
def get_users():
    with driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u.userId AS userId")
        users = [{"userId": record["userId"]} for record in result]
        return jsonify(users)

@app.route('/movies', methods=['GET'])
def get_movies():
    with driver.session() as session:
        result = session.run("MATCH (m:Movie) RETURN m.movieId AS movieId, m.title AS title")
        movies = [{"movieId": record["movieId"], "title": record["title"]} for record in result]
        return jsonify(movies)

@app.route('/ratings', methods=['GET'])
def get_ratings():
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User)-[r:RATED]->(m:Movie)
            RETURN u.userId AS userId, m.movieId AS movieId, r.rating AS rating
        """)
        ratings = [{"userId": record["userId"], "movieId": record["movieId"], "rating": record["rating"]} for record in result]
        return jsonify(ratings)

@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    movie_id = data.get("movieId")
    title = data.get("title")

    if not movie_id or not title:
        return jsonify({"error": "movieId and title are required"}), 400

    with driver.session() as session:
        session.run(
            "CREATE (m:Movie {movieId: $movieId, title: $title})",
            movieId=movie_id,
            title=title
        )
    return jsonify({"message": "Movie created successfully", "movieId": movie_id, "title": title}), 201

@app.route('/health', methods=['GET'])
def health():
    try:
        # Probar conexión a Neo4j
        with driver.session() as session:
            session.run("RETURN 1")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

