from flask import Flask, render_template, request, redirect, url_for, session
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os


app = Flask(__name__)
app.secret_key = "smartplantsecret"   # Needed for session


users = {}

# ===============================
# HOME PAGE
# ===============================
@app.route('/')
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", users=users)

# ===============================
# SIGNUP
# ===============================
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']

        if email in users:
            return render_template("signup.html",
                                   message="Email already exists!")

        # Store user details
        users[email] = {
            "fullname": fullname,
            "phone": phone,
            "password": password,
            "location": location
        }

        session["user"] = email  # Auto login after signup

        return redirect(url_for("home"))

    return render_template("signup.html")

# ===============================
# LOGIN
# ===============================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email]["password"] == password:
            session["user"] = email
            return redirect(url_for("home"))
        else:
            return render_template("login.html",
                                   message="Invalid email or password")

    return render_template("login.html")

@app.route('/rotation')
def rotation():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("rotation.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route('/detect')
def detect():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("detect.html")

@app.route('/upload/<crop>')
def upload(crop):
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("upload.html", crop=crop)

@app.route('/agri-shop')
def agri_shop():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("agri_shop.html")

# ===============================
# PREDICTION ROUTE
# ===============================
@app.route('/predict', methods=['POST'])
def predict():

    if "user" not in session:
        return redirect(url_for("login"))

    crop = request.form.get("crop")
    file = request.files['image']

    from werkzeug.utils import secure_filename

    file = request.files['image']

    upload_folder = "static"

# create folder if not exists
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    img = cv2.imread(filepath)

    # ===============================
    # LOAD MODEL + SET IMAGE SIZE
    # ===============================
    if crop == "paddy":
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "models", "PADDY.h5")

        model = load_model(model_path)
        class_names = [
            "bacterial_leaf_blight","bacterial_leaf_streak",
            "bacterial_panicle_blight","blast","brown_spot",
            "dead_heart","downy_mildew","hispa","normal","tungro"
        ]
        img_size = (224,224)
        from paddyrecom import get_solution

    elif crop == "maize":
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "models", "MAIZE.h5")

        model = load_model(model_path)
        class_names = ["Blight","Common_Rust","Gray_Leaf_Spot","Healthy"]
        img_size = (128,128)   # ✔ your maize training size
        from maizerecom import get_solution

    elif crop == "sugarcane":
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "models", "SUGARCANE.h5")

        model = load_model(model_path)
        class_names = ["Healthy","Mosaic","RedRot","Rust","Yellow"]
        img_size = (128,128)   # ✔ change if sugarcane trained differently
        from sugarcanerecom import get_solution

    # ===============================
    # NOW resize ONLY ONCE
    # ===============================
    img = cv2.resize(img, img_size)
    img = img / 255.0
    img = np.reshape(img, (1, img_size[0], img_size[1], 3))

    prediction = model.predict(img)
    predicted_class = class_names[np.argmax(prediction)]

    solution = get_solution(predicted_class)

    return render_template("result.html",
                           crop=crop,
                           prediction=predicted_class,
                           solution=solution)


# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    app.run(debug=True)