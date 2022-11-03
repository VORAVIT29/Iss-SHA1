import os
from flask import Flask, render_template, request
# import hashlib
from sha1 import Sha1

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("iss.html")


@app.route('/convert-text-sha1', methods=['POST'])
def text_to_sha1():
    mess = request.form.get("mess")

    # result = hashlib.sha1(mess.encode())
    # return result.hexdigest()
    result = Sha1()
    return result.call_sha1(mess)


@app.route('/', methods=['POST'])
def convet_files():
    if request.method == 'POST':
        files = request.files.getlist("formFileMultiple[]")
        # del
        for file_del in os.listdir(os.path.join(".\\file")):
            if os.listdir(os.path.join(".\\file")) not in []:
                os.remove(os.path.join(".\\file", file_del))

        # save
        for file in files:
            patch = os.path.join(".\\file", file.filename)
            file.save(patch)

        # open file
        text = ""
        for file in os.listdir(os.path.join(".\\file")):
            f = open(f".\\file\\{file}", "r", encoding="utf-8")
            text += f.read()

        results = Sha1()
    # results = hashlib.sha1(text.encode())
    # return render_template("iss.html", result=results.hexdigest())
    return render_template("iss.html", result=results.call_sha1(text))


if __name__ == '__main__':
    app.run(debug=True)
