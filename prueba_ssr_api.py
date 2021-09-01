import json

from flask import Flask, request, make_response, session, redirect, url_for
import requests


app = Flask(__name__)
app.secret_key = 'thisismysecretkey'


def error(error_dict, status=400):
    return make_response(error_dict, status)


@app.route("/members_only")
def members_only():
    if "user" not in session:
        return redirect(url_for("login"))
    my_id = request.args.get('id')
    if my_id is None or len(my_id) == 0:
        return error({'error': 'El id no fue ingresado'})
    base_url = "https://jsonplaceholder.typicode.com/posts?id="
    mi_url = base_url + my_id
    r = requests.get(url=mi_url)
    data = json.loads(r.text)
    print(mi_url)
    return data[0]



@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        # _check_correct_user_and_pass(request.form)
        session["user"] = request.form
        return redirect(url_for("user"))
    else:
        return {
            "message": "You have to login"
        }


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return user
    else:
        return redirect(url_for("login"))


if __name__ == '__main__':
    app.run()
