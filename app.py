from flask import Flask, Response, request, render_template, redirect, url_for
import torch
import pickle
import joblib
import os

# print(torch.cuda.is_available())
# print(torch.cuda.current_device())
# print(torch.cuda.get_device_name(0))


# with open('model.pkl', 'rb') as f:
#     m = pickle.load(f)
#     torch.load(f, map_location=torch.device('cpu'))

# loaded_model = joblib.load('checker.model')

# def load_model():
#   model = pickle.load(open('model.pkl','rb'))
#   return model
# model = load_model()

# with open('checker.model', 'rb') as f:
#     loaded_model = pickle.load(f)
#     torch.load(f, map_location=torch.device('cpu'))

# model.correct_from_file(src="sample_corrupt.txt")

# m.correct_from_file(src="sample_corrupt.txt")

app=Flask(__name__)

Allowed_Extensions = set(['txt'])

def check_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in Allowed_Extensions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    error = None
    filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file selected'
            return render_template('index.html', error=error)

        file = request.files['file']
        filename = file.filename

        if filename == '':
            error = 'No file selected'
            return render_template('index.html', error=error)

        if check_file(filename) == False:
            error = 'File extension not allowed'
            return render_template('index.html', error=error)

        file.save(os.path.join("uploads", filename))
    return render_template('index.html', filename = filename)

if __name__ == '__main__':
    app.run(debug=True)

# def get_prediction(model, input_data):
#     input_data = torch.tensor(input_data, dtype=torch.float32)
#     input_data = input_data.unsqueeze(0)
#     prediction = model(input_data)
#     return prediction.item()

# @app.route('/predict', methods=['POST'])
# def predict():
#     input_data = request.form.to_dict()
#     input_data = list(input_data.values())
#     input_data = list(map(float, input_data))
#     prediction = get_prediction(m, input_data)
#     return str(prediction)

