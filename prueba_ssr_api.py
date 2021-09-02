import json

from flask import Flask, request, make_response, redirect, url_for
import requests

session = []
app = Flask(__name__)
app.secret_key = 'thisismysecretkey'


def error(error_dict, status=400):
    return make_response(error_dict, status)


@app.route("/members_only")
def members_only():
    if request.json['user'] not in session:
        return redirect(url_for("login_get"))
    my_id = request.args.get('id')
    if my_id is None or len(my_id) == 0:
        return error({'error': 'You have to send the id'})
    base_url = "https://jsonplaceholder.typicode.com/posts?id="
    mi_url = base_url + my_id
    r = requests.get(url=mi_url)
    data = json.loads(r.text)
    return data[0]


def _check_correct_user_and_pass(user, password):
    for element in users:
        if element["user"] == user and element["password"] == password:
            return True
    return False


def _user_already_exists(user):
    for element in users:
        if element['user'] == user:
            return True
    return False


@app.route("/login", methods=["POST"])
def login_post():
    if _check_correct_user_and_pass(request.json['user'], request.json['password']):
        session.append(request.json['user'])
        return {
            "message": "Successfull login"
        }
    else:
        return {
            "message": "Wrong user or password"
        }


@app.route("/login")
def login_get():
    return {
            "message": "You have to login"
        }


@app.route("/logout", methods=["POST"])
def logout():
    if request.json['user'] not in session:
        return redirect(url_for("login_get"))
    session.remove(request.json['user'])
    return {
            "message": "Successfull logout"
        }


@app.route("/register", methods=["POST"])
def register():
    if _user_already_exists(request.json["user"]):
        return error({'error': 'This user already exists'})
    else:
        users.append({
            "user": request.json["user"],
            "password": request.json["password"]
        })
        return {"message": "Now you can login"}


def _user_in_session(my_user):
    for user in session:
        if user['user'] == my_user:
            return True


users = [
    {
        "user": "admin",
        "password": "admin"
    },
    {
        "user": "admin2",
        "password": "admin2"
    }
]


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return user
    else:
        return redirect(url_for("login"))


if __name__ == '__main__':
    app.run()
