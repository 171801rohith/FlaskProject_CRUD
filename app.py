from flask import Flask, request, redirect, url_for, render_template, flash
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/FlaskProject"
app.secret_key = "Rohith171801"
mongodb = PyMongo(app).db


class FlaskMongo:
    emailID = None

    def get_last_user():
        last_user = mongodb.UserDB.find().sort("UserID", -1).limit(1)
        last_user = list(last_user)
        if last_user:
            return last_user[0]["UserID"]
        else:
            return 100

    def increment():
        id = FlaskMongo.get_last_user()
        return id + 1

    @app.route("/")
    def index():
        return render_template("layout.html")

    @app.route("/signup", methods=["POST"])
    def sign_upHTML():
        return render_template("signup.html")

    @app.route("/create", methods=["POST"])
    def createHTML():
        return render_template("create.html")

    @app.route("/update", methods=["POST"])
    def updateHTML():
        userRev = mongodb.ReviewDB.find_one({"EmailID": FlaskMongo.emailID})
        if userRev:
            return render_template("update.html")
        else:
            flash("You have not reviewed the course yet. ")
            return render_template("crud.html")

    @app.route("/back")
    def curdHTML():
        return render_template("crud.html")

    @app.route("/logout", methods=["POST"])
    def log_out():
        return render_template("layout.html")

    @app.route("/signin", methods=["POST"])
    def sign_in():
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        userid = FlaskMongo.increment()

        check = mongodb.UserDB.find_one({"EmailID": email})
        if check:
            flash("Email already exists. Please try again.")
            return redirect(url_for("index"))

        mongodb.UserDB.insert_one(
            {
                "UserID": userid,
                "Name": name,
                "EmailID": email,
                "Password": password,
            }
        )

        flash(f"User Added Successfully. Your userID {userid}. Mail ID {email}")
        return redirect(url_for("index"))

    @app.route("/login", methods=["POST"])
    def login():
        FlaskMongo.emailID = request.form["email"]
        password = request.form["password"]
        user = mongodb.UserDB.find_one({"EmailID": FlaskMongo.emailID})
        if user:
            if user["Password"] == password:
                return render_template("crud.html")
            else:
                flash("Invalid Password. Please try again.")
                return redirect(url_for("index"))
        else:
            flash("Email not found. Please Sign Up.")
            return redirect(url_for("index"))

    @app.route("/createReview", methods=["POST"])
    def create_review():
        user = mongodb.UserDB.find_one({"EmailID": FlaskMongo.emailID})

        if user:
            userRev = mongodb.ReviewDB.find_one({"EmailID": FlaskMongo.emailID})
            if userRev:
                flash("You have already submitted a review.")
                return render_template("crud.html")
            else:
                review = request.form["review"]
                ratings = request.form["ratings"]
                mongodb.ReviewDB.insert_one(
                    {
                        "UserID": user["UserID"],
                        "Name": user["Name"],
                        "EmailID": user["EmailID"],
                        "Review": review,
                        "Ratings": ratings,
                    }
                )
            flash(f"Review Added Successfully. Your ratings {ratings}.")

        return render_template("crud.html")

    @app.route("/read", methods=["POST"])
    def read_review():
        userRev = mongodb.ReviewDB.find_one({"EmailID": FlaskMongo.emailID})
        if userRev:
            userID = userRev["UserID"]
            name = userRev["Name"]
            emailID = userRev["EmailID"]
            review = userRev["Review"]
            ratings = userRev["Ratings"]
            return render_template(
                "read.html",
                UserID=userID,
                Name=name,
                EmailID=emailID,
                Review=review,
                Ratings=ratings,
            )
        else:
            flash("You have not reviewed the course yet. ")
        return render_template("crud.html")

    @app.route("/delete", methods=["POST"])
    def delete_review():
        userRev = mongodb.ReviewDB.find_one({"EmailID": FlaskMongo.emailID})
        if userRev:
            userID = userRev["UserID"]
            name = userRev["Name"]
            emailID = userRev["EmailID"]
            review = userRev["Review"]
            ratings = userRev["Ratings"]
            mongodb.ReviewDB.delete_one(userRev)
            return render_template(
                "delete.html",
                UserID=userID,
                Name=name,
                EmailID=emailID,
                Review=review,
                Ratings=ratings,
            )
        else:
            flash("You have not reviewed the course yet. ")
        return render_template("crud.html")

    @app.route("/updateReview", methods=["POST"])
    def update_review():

        userRev = mongodb.ReviewDB.find_one({"EmailID": FlaskMongo.emailID})
        if userRev:
            review = request.form["review"]
            ratings = request.form["ratings"]
            mongodb.ReviewDB.update_one(
                {"EmailID": userRev["EmailID"]},
                {
                    "$set": {
                        "UserID": userRev["UserID"],
                        "Name": userRev["Name"],
                        "Review": review,
                        "Ratings": ratings,
                    }
                },
                upsert=False,
            )
            flash(f"Review Updated Successfully. Your updated ratings {ratings}.")
        else:
            flash("You have not reviewed the course yet. ")

        return render_template("crud.html")


if __name__ == "__main__":
    app.run(debug=True)
