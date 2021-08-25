from flask import Flask, render_template, request
from Switcher.switcher import Switcher

app = Flask(__name__)

# main run, runs switcher first, if can't connect doesn't run server
if __name__ == "__main__":
    # switcher = Switcher("junior", "project")
    # logger = switcher.logger
    # logger.append(logger.get_time() + "Server started.")
    # switcher.run()
    app.run()


def render_index():
    data = {'name': 'სახელი', 'surname': 'გვარი'}
    return render_template("index.html", data=data)


@app.route('/')
def main_page():
    return render_index()


# with app.app_context('/'):
@app.route('/switch', methods=['POST'])
def switch():
    data = request.form
    # print(data.getlist())
    dct = data.to_dict()
    print(dct.get("num"))
    # print(dct.get("state"))
    return render_index()


@app.route('/switch', methods=['GET'])
def switch_redirect():
    return main_page
