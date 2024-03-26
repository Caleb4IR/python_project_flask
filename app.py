import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
import uuid

load_dotenv()
pprint(os.environ.get("AZURE_DATABASE_URL"))

app = Flask(__name__)
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

db = SQLAlchemy(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)

movies = [
    {
        "id": "99",
        "name": "Vikram",
        "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
        "rating": 8.4,
        "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
        "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
    },
    {
        "id": "100",
        "name": "RRR",
        "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
        "rating": 8.8,
        "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
        "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
    },
    {
        "id": "101",
        "name": "Iron man 2",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
        "rating": 7,
        "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
        "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
    },
    {
        "id": "102",
        "name": "No Country for Old Men",
        "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
        "rating": 8.1,
        "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
        "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
    },
    {
        "id": "103",
        "name": "Jai Bhim",
        "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
        "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
        "rating": 8.8,
        "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
    },
    {
        "id": "104",
        "name": "The Avengers",
        "rating": 8,
        "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
        "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
        "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
    },
    {
        "id": "105",
        "name": "Interstellar",
        "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
        "rating": 8.6,
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
    },
    {
        "id": "106",
        "name": "Baahubali",
        "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
        "rating": 8,
        "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
        "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
    },
    {
        "id": "107",
        "name": "Ratatouille",
        "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
        "rating": 8,
        "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
        "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
    },
    {
        "name": "PS2",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
        "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
        "rating": 8,
        "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
        "id": "108",
    },
    {
        "name": "Thor: Ragnarok",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
        "rating": 8.8,
        "trailer": "https://youtu.be/NgsQ8mVkN8w",
        "id": "109",
    },
]

# jinja2 - templates

user = {
    "name": "Caleb",
    "pic": "https://play-lh.googleusercontent.com/C9CAt9tZr8SSi4zKCxhQc9v4I6AOTqRmnLchsu1wVDQL0gsQ3fmbCVgQmOVM1zPru8UH=w240-h480-rw",
}

name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming"]

users = [
    {
        "name": "Caleb",
        "pic": "https://play-lh.googleusercontent.com/C9CAt9tZr8SSi4zKCxhQc9v4I6AOTqRmnLchsu1wVDQL0gsQ3fmbCVgQmOVM1zPru8UH=w240-h480-rw",
        "pro": True,
    },
    {
        "name": "Gemma",
        "pic": "https://media.licdn.com/dms/image/D4E03AQHsOoHTvwR6LA/profile-displayphoto-shrink_200_200/0/1691159741445?e=2147483647&v=beta&t=DFLLEtLkOrJdn9QnYZaoXFkmihckM4-6MDZ5sqq8xR4",
        "pro": False,
    },
    {
        "name": "Rashay",
        "pic": "https://media.licdn.com/dms/image/D4D03AQEYHIa8t0EBFQ/profile-displayphoto-shrink_200_200/0/1674318245732?e=2147483647&v=beta&t=2_A4sayvdZfZWVftQONBYkZxh6p1wCt2AVBBTxXVIsc",
        "pro": True,
    },
]

# Model (SQLAlchemy) == Schema

# CREATE TABLE movies (
#     id VARCHAR(50) PRIMARY KEY,
#     name VARCHAR(100),
#     poster VARCHAR(255),
# 	rating FLOAT,
#     summary VARCHAR(500),
#     trailer VARCHAR(255)
# );


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100))
    poster = db.Column(db.String(255))
    rating = db.Column(db.Float)
    summary = db.Column(db.String(500))
    trailer = db.Column(db.String(255))

    # JSON Keys
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "rating": self.rating,
            "summary": self.summary,
            "trailer": self.trailer,
        }


# GET --> /movies --> JSON
@app.get("/movies")
def get_movies():
    movie_list = Movie.query.all()  # SELECT * FROM movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # to list of dictionaries
    return jsonify(data)


# Task 1
# .all() -.get()
@app.get("/movies/<id>")
def get_movies_by_id(id):
    movie = Movie.query.get(id)
    if movie:
        return jsonify(movie.to_dict())
    else:
        return jsonify({"message": "Movie not found"}), 404


# Task 2 display the data on the page
@app.route("/movie-list")
def movie_list_page():
    movie = Movie.query.all()
    return render_template("movie-list.html", movies=movie)


# Task 3 display the data on the page from Azure
@app.route("/movie-list/<id>")
def movie_detail_page(id):
    movie = Movie.query.get(id)
    if movie:
        return render_template("movie-detail.html", movie=movie)
    else:
        return "Movie not found", 404


# Task 4 | db.session.delete(<movie>)
@app.delete("/movies/<id>")
def delete_movies(id):
    deleted_movie = Movie.query.get(id)

    if not deleted_movie:
        return jsonify({"message": "Movie not found"}), 404

    try:
        db.session.delete(deleted_movie)
        db.session.commit()  # Make the change permanent
        return jsonify(
            {"message": "Movie deleted sucessfully", "data": deleted_movie.to_dict()}
        )
    except Exception as e:
        db.session.rollback()  # Undo the change
        return jsonify({"message": str(e)}), 500


# @app.post("/movies")
# def post_movies():
#     data = request.json
#     new_movie = Movie(
#         name=data["name"],
#         poster=data["poster"],
#         rating=data["rating"],
#         summary=data["summary"],
#         trailer=data["trailer"],
#     )

#     try:
#         db.session.add(new_movie)
#         db.session.commit()
#         movies.append(data)
#         result = {"message": "Added successfully", "data": new_movie.to_dict()}
#         return jsonify(result), 201
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": str(e)}), 500


@app.post("/movies")
def post_movies():
    data = request.json
    new_movie = Movie(**data)  # Only works when key matches value and id is not givens

    try:
        db.session.add(new_movie)
        db.session.commit()
        movies.append(data)
        result = {"message": "Added successfully", "data": new_movie.to_dict()}
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Task: convert to db call
@app.put("/movies/<id>")
def update_movie_by_id(id):
    data = request.json

    movie_to_update = Movie.query.get(id)
    try:
        # movie_to_update.name = data.get("name", movie_to_update.name)
        # movie_to_update.poster = data.get("poster", movie_to_update.poster)
        # movie_to_update.rating = data.get("rating", movie_to_update.rating)
        # movie_to_update.summary = data.get("summary", movie_to_update.summary)
        # movie_to_update.trailer = data.get("trailer", movie_to_update.trailer)

        for key, value in data.items():
            if hasattr(movie_to_update, key):
                setattr(movie_to_update, key, value)

        db.session.commit()
        return jsonify({"message": "Movie updated", "data": movie_to_update.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Task 5 | Delete on the web page
@app.route("/movie-ist/delete", methods=["POST"])
def delete_movie_by_id():
    print(id)
    return "<p>Movie deleted successfully! 😎</p>"


@app.route("/")
def hello_world():
    return "<p>Hello, Sanlam! 😎</p>"


@app.route("/about")
def about():
    return render_template("about.html", users=users)


@app.route("/profile")
def profile():
    return render_template("profile.html", name=name, hobbies=hobbies)


# Task
# Goto -> http://127.0.0.1:5000/movie-list/100 -> Detail of that particular movie alone


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("forms.html")


@app.route("/dashboard", methods=["POST"])
def dashboard_page():
    username = request.form.get("username")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return f"<h1>Hi {username}</h1>"


# Task - /movies/add -> Add movie form (5 fields) -> Submit -> /movies-list
@app.route("/movies/add", methods=["GET"])
def add_movie_form():
    return render_template("add_movie.html")


@app.route("/movies/add", methods=["POST"])
def add_movie():
    movie_ids = [int(movie["id"]) for movie in movies]
    max_id = max(movie_ids)
    next_id = str(max_id + 1)

    title = request.form["title"]
    poster = request.form["poster"]
    summary = request.form["summary"]
    rating = request.form["rating"]
    trailer = request.form["trailer"]

    new_movie = {
        "id": next_id,
        "name": title,
        "poster": poster,
        "summary": summary,
        "rating": rating,
        "trailer": trailer,
    }

    db.session.add(new_movie)
    db.session.commit()

    return {"message": "Added successfully", "data": new_movie.to_dict()}


# Task - Welcome message

# Task 1
# <variable name> | id --> keyword argument
# @app.get("/movies/<id>")
# def get_movies(id):
#     for movie in movies:
#         if movie["id"] == id:
#             return jsonify(movie)


# # OR
# @app.get("/movies/<id>")
# def get_movies(id):
#     filtered_movie = [movie for movie in movies if movie["id"] == id]
#     return jsonify(filtered_movie[0])


# OR
# @app.get("/movies/<id>")
# def get_movies(id):
#     # Generator expression () | Find an item list | next(expression, default_value)
#     # Advantage: Loop will
#     filtered_movie = next((movie for movie in movies if movie["id"] == id), None)
#     return jsonify(filtered_movie)


# Task 1.1 - Negative scenario
# message - movie not found | status_code - 404


# Task - 2
# Create Delete API for movies
# @app.delete("/movies/<id>")
# def delete_movies(id):
#     #Permission to modify the lexical scope variable | reassign not allowed
#     global movies
#     movies = [movie for movie in movies if movie["id"]!= id]
#     return jsonify({"message": "Movie deleted successfully"})

# OR

# @app.delete("/movies/<id>")
# def delete_movies(id):
#     deleted_movie = next((movie for movie in movies if movie["id"] == id), None)
#     movies.remove(deleted_movie)
#     return jsonify({"message": "Movie deleted successfully"})


# Task - 2.1 Negative scenario
# Create Delete API for movies
# @app.delete("/movies/<id>")
# def delete_movies(id):
#     deleted_movie = next((movie for movie in movies if movie["id"] == id), None)
#     if deleted_movie:
#         movies.remove(deleted_movie)
#         return jsonify({"message": "Movie deleted sucessfully", "data": deleted_movie})
#     else:
#         return jsonify({"message": "Movie not found"}), 404


# Task
# Update a movie
# @app.put("/movies/<id>")
# def update_movie_by_id(id):
#     data = request.json

#     movie_to_update = next((movie for movie in movies if movie["id"] == id), None)
#     if movie_to_update:
#         movie_to_update.update(data)
#         return jsonify({"message": "Movie updated", "data": movie_to_update})
#     else:
#         return jsonify({"message": "Movie not updated"}), 404


# @app.put("/movies/<id>")
# def update_movie_by_id(id):
#     movie_idx = next((idx for idx, movie in enumerate(movies) if movie["id"] == id), None) # same memory
#     body = request.json
#     movies[movie_idx] = {**movies[movie_idx], **body}

# @app.post("/movies")
# def post_movies():
#     data = request.json
#     movies.append(data)
#     result = {"message": "Added Successfully"}
#     return jsonify(result), 201


# 1 more than the max id
# @app.post("/movies")
# def post_movies():
#     data = request.json

#     movie_ids = [int(movie["id"]) for movie in movies]
#     max_id = max(movie_ids)
#     next_id = str(max_id + 1)

#     data["id"] = next_id

#     movies.append(data)
#     result = {"message": "Added successfully", "data": data}
#     return jsonify(result), 201
