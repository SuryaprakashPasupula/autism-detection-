from flask import Flask, render_template, request, redirect,session,url_for, flash # type: ignore
import joblib # type: ignore
import string
import Database
import warnings
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array # type: ignore
from PIL import UnidentifiedImageError
import numpy as np
from PIL import Image




app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Needed for flashing messages

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        a=Database.Login(username,password)
        if a!=0:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username', 'error')
    return render_template('login.html')
@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        a=Database.Signup(username,password)
        if a!=0:
            flash('Account created', 'success')
            return render_template('login.html')
        else:
            flash('Invalid username', 'error')
    return render_template('Signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        result = request.form['result']
        # Here you can process the result as needed, for now, let's just show it in a popup
        flash(f'Result: {result}', 'info')
    return render_template('dashboard.html')

photo_size = 224

# Load the trained model
model = tf.keras.models.load_model("/Users/suryareddy/Desktop/autism prediction/model/autism_detection_modelAST.h5")

# Define class labels
#class_labels = {'non_autistic': 0, 'autistic': 1}

# Define function for preprocessing image
def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))  # Resize image to match model input size
    img_array = np.array(img)
    img_array = img_array / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Define function for making predictions
def predict_image(image_path):
    # Preprocess the image
    img_array = preprocess_image(image_path)

    # Make prediction
    prediction = model.predict(img_array)

    # Process prediction result
    result = 'Autistic' if prediction[0][0] > 0.5 else 'Non-autistic'
    
    return result


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the uploaded file
        uploaded_file = request.files['file']

        # Save the uploaded file
        image_path = "uploaded_image.jpg"
        uploaded_file.save(image_path)

        # Make prediction
        predicted_class = predict_image(image_path)  # Fixed function name here

        # Clear previous flashes and flash the predicted class
        session.pop('_flashes', None)
        flash(f'Predicted class: {predicted_class}')

        return render_template('output.html', predicted_class=predicted_class)

    except UnidentifiedImageError:
        # Handle the case where the uploaded file is not a valid image
        return 'Error: Uploaded file is not a valid image.'
if __name__ == '__main__':
    app.run()
