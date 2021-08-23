from flask import Flask, render_template, request
from Switcher.switcher import Switcher
app = Flask(__name__)

logger = Switcher.logger

@app.route('/')
def main_page():
    return render_template("index.html")


# with app.app_context('/'):

@app.route('/switch', methods=['POST', 'GET'])
def switch():
    if request.method == 'GET':
        return main_page
    if request.method == 'POST':
        data = request.form
        # print(data.getlist())
        dct = data.to_dict()
        print(dct.get("num"))
        print(dct.get("state"))
        return render_template("index.html")


if __name__ == '__main__':
    app.run()
