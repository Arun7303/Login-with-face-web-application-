import os
import datetime
import cv2
import face_recognition
from flask import Flask, jsonify, request, render_template, redirect

app = Flask(__name__)

registered_data = {}


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    photo = request.files['photo']

    uploads_folder = os.path.join(os.getcwd(), "static", "uploads")

    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    photo.save(os.path.join(uploads_folder,
               f'{datetime.date.today()}_{name}.jpg'))
    registered_data[name] = f"{datetime.date.today()}_{name}.jpg"

    response = {"success": True, 'name': name}
    return jsonify(response)


@app.route("/login", methods=["POST"])
def login():
    photo = request.files['photo']

    uploads_folder = os.path.join(os.getcwd(), "static", "uploads")

    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    login_filename = os.path.join(uploads_folder, "login_face.jpg")

    photo.save(login_filename)

    login_image = cv2.imread(login_filename)
    gray_image = cv2.cvtColor(login_image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        response = {"success": False}
        return jsonify(response)

    login_image = face_recognition.load_image_file(login_filename)
    login_face_encodings = face_recognition.face_encodings(login_image)

    for name, filename in registered_data.items():
        registered_photo = os.path.join(uploads_folder, filename)
        registered_image = face_recognition.load_image_file(registered_photo)
        registered_face_encodings = face_recognition.face_encodings(
            registered_image)

        if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
            matches = face_recognition.compare_faces(
                registered_face_encodings, login_face_encodings[0])

            if any(matches):
                # Include user's name in response
                return render_template('success.html', user_name=name)

    response = {"success": False}
    return jsonify(response)


@app.route("/success")
def success():
    user_name = request.args.get("user_name")
    return render_template("success.html", user_name=user_name)


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/forget")
def forget_password():
    return render_template("forget.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
