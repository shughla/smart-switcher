from flask import Flask, render_template, request, session
from Switcher.switcher import Switcher
import sys  # for debugging purposes

app = Flask(__name__)
# change to something else before running on local machine
# generated using following code:
# import os
# os.urandom(24)

app.secret_key = '\xb8\x02\xc2\x16RH\xdftt=\x04\x05\x06yE>\n\xe1\xfc}\xa5\xc3\x9f\xac'
app.config['SESSION_TYPE'] = "filesystem"

authenticated = "authenticated"


# main run, runs switcher first, if can't connect doesn't run server


def render_main():
    # this needs to be normal render_template login.html
    # and data needs to be on render_boxes
    data = dict()
    for i in range(10):
        data["val" + str(i)] = str(i)
    return render_template("index.html", data=data)  # =data is dictionary.


def is_authenticated() -> bool:
    return session.get(authenticated) is not None


def get_admin_credentials():
    admin_accounts = dict()
    try:
        with open("Data/admin.txt", "r") as f:
            for line in f:
                line = line.strip(" \n")
                if line == "":
                    continue
                line = line.split(":", 2)
                admin_accounts[line[0]] = line[1]
        return admin_accounts
    except FileNotFoundError:
        print("Data/admin.txt doesn't exist.", file=sys.stderr)
        return admin_accounts


def authenticate(username, password):
    admin_accounts = get_admin_credentials()
    if admin_accounts.get(username) == password:
        session[authenticated] = True
        return True
    return False


def terminal_print(string):
    print(string, file=sys.stderr)


@app.route('/logout')
def logout():
    if session.get(authenticated) is not None:
        session[authenticated] = None
    return render_main()


@app.route('/')
def main_page():
    return render_main()


# after logging in
@app.route('/boxes', methods=['POST'])
def login_page():
    username = request.form.get("username")
    password = request.form.get("password")
    authenticate(username, password)
    return render_if_authenticated("boxes.html")


def render_if_authenticated(template_name):
    if not is_authenticated():
        return render_main()
    return render_template(template_name)


@app.route('/boxes', methods=['GET'])
def main_menu():
    return render_if_authenticated("boxes.html")


# with app.app_context('/'):
@app.route('/switch', methods=['POST'])
def switch():
    data = request.form
    dct = data.to_dict()
    return render_main()


@app.route("/box", methods=['GET'])
def box_page():
    return render_if_authenticated("box.html")


@app.route('/switch', methods=['GET'])
def switch_redirect():
    return render_if_authenticated("switch.html")
