import json

from flask import Flask, request, make_response, redirect, url_for
import requests

session = []
app = Flask(__name__)
app.secret_key = 'thisismysecretkey'


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



def error(error_dict, status=400):
    return make_response(error_dict, status)


@app.route("/members_only")
def members_only():
    if not(_user_in_session(request.json['user'])):
        return redirect(url_for("login_get"))
    my_id = request.args.get('id')
    if my_id is None or len(my_id) == 0:
        return error({'error': 'You have to send the id'})
    base_url = "https://jsonplaceholder.typicode.com/posts?id="
    mi_url = base_url + my_id
    r = requests.get(url=mi_url)
    data = json.loads(r.text)
    return data[0]


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
    if not(_user_in_session(request.json['user'])):
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
    return any(list(filter(lambda user: user == my_user, session)))


def _check_correct_user_and_pass(user, password):
    return any(list(filter(lambda element: element['user'] == user and element['password'] == password, users)))


def _user_already_exists(my_user):
    return any(list(filter(lambda user: user['user'] == my_user, users)))


@app.route("/user")
def user():
    if not(_user_in_session(request.json['user'])):
        return redirect(url_for("login_get"))
    return request.json['user']


if __name__ == '__main__':
    app.run()
