from flask import request, redirect, url_for, render_template, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, mongodb

from WTForms.loginForm import LoginForm, SignUpButton
from WTForms.crudForm import CRUDForm
from WTForms.createReviewForm import CreateReviewForm
from WTForms.updateForm import UpdateForm
from WTForms.signupForm import SignupForm


class FlaskMongo:

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
        return render_template(
            "layout.html", loginForm=LoginForm(), signUpButton=SignUpButton()
        )

    @app.route("/signup", methods=["POST"])
    def sign_upHTML():
        return render_template("signup.html", signupForm=SignupForm())

    @app.route("/create", methods=["POST", "GET"])
    def createHTML():
        if "emailID" in session:
            return render_template("create.html", createReviewForm=CreateReviewForm())
        else:
            return redirect(url_for("index"))

    @app.route("/update", methods=["POST", "GET"])
    def updateHTML():
        if "emailID" in session:
            userRev = mongodb.ReviewDB.find_one({"EmailID": session.get("emailID")})
            if userRev:
                return render_template("update.html", updateForm=UpdateForm())
            else:
                flash("You have not reviewed the course yet. ")
                return render_template("crud.html", crudForm=CRUDForm())
        else:
            return redirect(url_for("index"))

    @app.route("/back")
    def curdHTML():
        return render_template("crud.html", crudForm=CRUDForm())

    @app.route("/logout", methods=["POST"])
    def log_out():
        flash("Logged out successfully.")
        session.pop("emailID", None)
        return redirect(url_for("index"))

    @app.route("/signin", methods=["POST"])
    def sign_in():
        signupForm = SignupForm()
        if signupForm.validate_on_submit():
            name = signupForm.name.data
            email = signupForm.emailID.data
            password = generate_password_hash(signupForm.password.data)
            signupForm.name.data = ""
            signupForm.emailID.data = ""
            signupForm.password.data = ""
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
        loginForm = LoginForm()
        if loginForm.validate_on_submit():
            email = loginForm.emailID.data
            password = loginForm.password.data
            loginForm.emailID.data = ""
            loginForm.password.data = ""
            user = mongodb.UserDB.find_one({"EmailID": email})
            if user:
                if check_password_hash(user["Password"], password):
                    session.permanent = True
                    session["emailID"] = email

                    return render_template("crud.html", crudForm=CRUDForm())
                else:
                    flash("Invalid Password. Please try again.")
                    return redirect(url_for("index"))
            else:
                flash("Email not found. Please Sign Up.")
                return redirect(url_for("index"))

    @app.route("/createReview", methods=["POST"])
    def create_review():
        if "emailID" in session:
            user = mongodb.UserDB.find_one({"EmailID": session.get("emailID")})

            if user:
                userRev = mongodb.ReviewDB.find_one({"EmailID": session.get("emailID")})
                if userRev:
                    flash("You have already submitted a review.")
                    return render_template("crud.html", crudForm=CRUDForm())
                else:
                    createReviewForm = CreateReviewForm()
                    if createReviewForm.validate_on_submit():
                        review = createReviewForm.review.data
                        ratings = createReviewForm.ratings.data
                        createReviewForm.review.data = ""
                        createReviewForm.ratings.data = ""
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

            return render_template("crud.html", crudForm=CRUDForm())
        else:
            return redirect(url_for("index"))

    @app.route("/read", methods=["POST", "GET"])
    def read_review():
        if "emailID" in session:
            userRev = mongodb.ReviewDB.find_one({"EmailID": session.get("emailID")})
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
            return render_template("crud.html", crudForm=CRUDForm())
        else:
            return redirect(url_for("index"))

    @app.route("/delete", methods=["POST", "GET"])
    def delete_review():
        if "emailID" in session:
            userRev = mongodb.ReviewDB.find_one({"EmailID": session.get("emailID")})
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
            return render_template("crud.html", crudForm=CRUDForm())
        else:
            return redirect(url_for("index"))

    @app.route("/updateReview", methods=["POST"])
    def update_review():
        if "emailID" in session:
            userRev = mongodb.ReviewDB.find_one({"EmailID": session.get("emailID")})
            if userRev:
                updateForm = UpdateForm()
                if updateForm.validate_on_submit():
                    review = updateForm.review.data
                    ratings = updateForm.ratings.data
                    updateForm.review.data = ""
                    updateForm.ratings.data = ""
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
                    flash(
                        f"Review Updated Successfully. Your updated ratings {ratings}."
                    )
            else:
                flash("You have not reviewed the course yet. ")

            return render_template("crud.html", crudForm=CRUDForm())
        else:
            return redirect(url_for("index"))
