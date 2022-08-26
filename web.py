import json
import os
from flask import Flask, redirect, url_for, render_template, request, flash
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/image/upload'
ALLOWED_EXTENSIONS = { 'jpg', 'jpeg', 'jfif','png','webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        imgInput = upload_file()
        bgrevomer(imgInput)
        return redirect(url_for("image", n=imgInput))
    else:
        return render_template("login.html")



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def upload_file():
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        return filename


def bgrevomer(input_name):
    Name = input_name
    outputName = input_name.split('.')[0]
    outputName = outputName.replace(" ", "-")
    input_path = os.path.join(UPLOAD_FOLDER,Name)
    output_path = f'static\image\edit_bg\{outputName}.png'
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)


@app.route("/<n>")
def image(n):
    outputName = n.split('.')[0]
    outputName = outputName.replace(" ", "-")
    output_path = f'static\\image\\edit_bg\\{outputName}.png'
    #output_path = output_path.replace("\\\\", "\\")
    #return {"file_name": output_path, "status": 200}
    return render_template("image.html", outpath=output_path)


if __name__ == "__main__":
    app.run(debug=True)
