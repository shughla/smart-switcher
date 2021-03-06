from flask import Flask, render_template, request, session, Response, url_for
from Switcher.switcher import Switcher
from Switcher.box import Box
from Switcher.switch import Switch
from hmac import compare_digest
from Switcher.switcher import log_message
import sys  # for debugging purposes
import json

app = Flask(__name__)
# change to something else before running on local machine
# generated using following code:
# import os
# os.urandom(24)

app.secret_key = '\xb8\x02\xc2\x16RH\xdftt=\x04\x05\x06yE>\n\xe1\xfc}\xa5\xc3\x9f\xac'
app.config['SESSION_TYPE'] = "filesystem"
authenticated = "authenticated"
switcher = Switcher("junior", "project")
switcher.run()
disable_authentication = False
# main run, runs switcher first, if can't connect doesn't run server

if __name__ == "__main__":
    switch = Switch("ლევანას ოთახი", 1, 1)
    switcher.change_data_path("/Data/data.json")
    box = Box("ეს არის ლევანას სახლის ბოქსი ", [switch])
    switcher.save_data(box.toJSON())
    r = switcher.get_data()
    print(r["switch_array"][0]["name"])


def render_login():
    # this needs to be normal render_template login.html
    # and data needs to be on render_boxes
    data = dict()
    # for i in range(10):
    #     data["val" + str(i)] = str(i)
    return render_template("index.html", data=data)  # =data is dictionary.


def is_authenticated() -> bool:
    return disable_authentication or session.get(authenticated) is not None


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
    admin_password = admin_accounts.get(username)
    if admin_password is not None and compare_digest(admin_password, password):
        session[authenticated] = True
        return True
    return False


def terminal_print(string):
    print(string, file=sys.stderr)


@app.route('/logout')
def logout():
    if session.get(authenticated) is not None:
        session[authenticated] = None
    return render_login()


@app.route('/add_block', methods=['POST'])
def add_block():
    description = request.form.get("description")
    switcher.add_block(Box(description))
    return render_main_page()


@app.route('/')
def main_page():
    return render_login()


def render_main_page():
    data = switcher.get_data()
    return render_if_authenticated("boxes.html", data=data)


# after logging in
@app.route('/boxes', methods=['POST'])
def login_page():
    username = request.form.get("username")
    password = request.form.get("password")
    authenticate(username, password)
    return render_main_page()


def respond_if_authenticated(content, mimetype=None):
    if not is_authenticated():
        return render_login()
    if mimetype is not None:
        return Response(content)
    return Response(content, mimetype=mimetype)


def render_if_authenticated(template_name, data=None, data2=None, data3=None, sensor_diff=None):
    if not is_authenticated():
        return render_login()
    return render_template(template_name, data=data, data2=data2, data3=data3, sensor_diff=sensor_diff)


@app.route('/check', methods=['GET'])
@app.route('/edit', methods=['GET'])
@app.route('/add_switcher', methods=['GET'])
@app.route('/boxes', methods=['GET'])
@app.route('/box', methods=['GET'])
@app.route('/switch', methods=['GET'])
@app.route('/delete_box', methods=['GET'])
@app.route('/edit_box_name', methods=['GET'])
def main_menu():
    return render_main_page()


@app.route('/logs', methods=['POST', 'GET'])
def log_page():
    response = """<!DOCTYPE html><html lang="en">
                <head><meta charset="UTF-8">
                <title>logs</title>
                <a href="/boxes" class="go-back" >უკან დაბრუნება</a>
                <link rel= "stylesheet" type= "text/css" href= "{{url_for('static', filename='styles/main.css')}}">
                <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
                </head>
                <body style="overflow: auto;"><h1>Logs:</h1>"""
    with open("/home/shug/Desktop/smart-switcher/SwitcherWebServer/static/logs/log", "r") as f:
        response += "<br>".join(f.readlines())
    response += """</body>
                    <script type="text/javascript">window.scrollTo(0,document.body.scrollHeight);
                    </script>
                    </html>"""
    return respond_if_authenticated(response, mimetype='text/html')


@app.route('/add_switcher', methods=['POST'])
def add_switcher():
    box_index = int(request.values.get("box_index"))
    boxes = switcher.get_data_store().main_data
    switch_index = len(boxes[box_index].switch_array)
    switcher_name = request.values.get("switcher_name")
    new_switch = Switch(switcher_name, switch_index, False)
    switcher.add_switcher(box_index, new_switch)
    displayed_box = switcher.get_data()[box_index]
    return render_if_authenticated("box.html", displayed_box, box_index, switcher.data_store.get_switches(box_index))


@app.route('/box', methods=['POST'])
def box_page():
    index = get_index(request)
    return render_if_authenticated("box.html", switcher.get_boxes()[index], index,
                                   switcher.get_switchers(index))


@app.route('/check', methods=['POST'])
def get_sensor_values():
    box_index = int(request.values.get("box_index"))
    sensor_output = switcher.get_statuses(box_index)  # can be None
    displayed_box = switcher.get_data()[box_index]
    diff = None
    if sensor_output is not None:
        diff = []
        for i in range(len(displayed_box.switch_array)):
            diff.append(False)  # means it's normal
            if sensor_output[i].status != displayed_box.switch_array[i].status:
                diff[i] = True  # means it's different
                log_message("Changed - switch:" + str(i) +
                            ". status - Was:" + str(not bool(sensor_output[i])) +
                            " Is: " + str(bool(sensor_output[i].status)))
                switcher.update_switch(box_index, i, sensor_output[i].status)

    return render_if_authenticated("box.html", displayed_box, box_index,
                                   switcher.data_store.get_switches(box_index), diff)


@app.route('/send_check', methods=['POST'])
def check_sensors():
    box_index = int(request.values.get("box_index"))
    displayed_box = switcher.get_data()[box_index]
    switcher.check_statuses(box_index)
    return render_if_authenticated("box.html", displayed_box, box_index,
                                   switcher.data_store.get_switches(box_index))


def get_index(req: request):
    index = "error"
    for k in req.values:
        if len(k) == 0:
            continue
        index = int(k)
        break
    return index


@app.route('/update_box_name', methods=['POST'])
def update_box_name():
    box_name = request.form.get("box_name")
    box_index = int(request.values["data2"])
    switcher.update_box_name(box_index, box_name)
    displayed_box = switcher.get_data()[box_index]
    return render_if_authenticated("edit.html", displayed_box, box_index, switcher.get_switchers(box_index))


@app.route('/edit_switch_name', methods=['POST'])
def edit_switch_name():
    name = request.form.get("new_name")
    index = int(request.values["index"])
    box_index = int(request.values["data2"])
    switcher.update_name(box_index, index, name)
    displayed_box = switcher.get_data()[box_index]
    return render_if_authenticated("edit.html", displayed_box, box_index, switcher.get_switchers(box_index))


@app.route('/delete_switch', methods=['POST'])
def edit_page():
    index = int(request.values["index"])
    box_index = int(request.values["data2"])
    switcher.remove_switcher(box_index, index)
    displayed_box = switcher.get_data()[box_index]
    return render_if_authenticated("edit.html", displayed_box, box_index, switcher.get_switchers(box_index))


@app.route('/delete_box', methods=['POST'])
def delete_box():
    box_index = int(request.values["data2"])
    switcher.remove_box(box_index)
    return render_main_page()


@app.route('/edit', methods=['POST'])
def goto_edit_page():
    box_index = int(request.values["data2"])
    displayed_box = switcher.get_data()[box_index]
    return render_if_authenticated("edit.html", displayed_box, box_index, switcher.get_switchers(box_index))


@app.route('/switch', methods=['POST'])
def switch_redirect():
    index = int(request.values["idx"])
    status = request.form.get("check")
    if status == "on":
        status = 1
    else:
        status = 0
    switcher.switch_to(index, status)
    return render_main_page()  # doesn't do anything because page just doesn't redirect
