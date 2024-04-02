from flask import Flask,render_template,request,send_from_directory
from Data import Dataset,Doctor
from PIL import Image
from a import prediction
import socket
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/svg/<path:svg_path>')
def logo(svg_path):
    return send_from_directory('static', svg_path)

@app.route('/upload_patient',methods=['POST'])
def patient_data():
    if 'file' not in request.files:
        return render_template('patient.html')
    file = request.files['file']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    contact = request.form['phn']
    img = Image.open(file)
    result = prediction(img)
    message = [[f'Name : {name}'],[f'Gender : {gender}'],[f'Age : {age}'],[f'File Name : {file.filename}'],[f'Result :{result}']]
    data = [name,gender,age,file.filename,result]
    dataset = Dataset(name=name,age=age,gender=gender,file_name=file.filename, contact=contact, result=result)
    if file:
        dataset.add(name=name, age=age,gender=gender,file_name=file.filename, contact=contact, result=result).save()
        return render_template('patient.html',message=message,data=data) 

@app.route('/patient')
def patient():
    names = ['','','','','','']
    return render_template('patient.html',data=names)


@app.route('/upload_doctor', methods=['POST'])
def doctor_data():
    if 'file' not in request.files:
        return render_template('doctor.html', message=["Error: No file uploaded"])
    
    files = request.files.getlist('file')  # Use getlist() to handle multiple file uploads
    doctor_files = [file.filename for file in files]
    pred = []
    rates = []
    for file in files:
        # Read the image file and encode it as base64
        img = Image.open(file)
        result = prediction(img)
        pred.append(result)
    Doctor(files=doctor_files,reports=pred, rate=rates)
    message = [[f'File Name : {doctor_files}'],[f'Result : {pred}']]
    # df={
    #     "files":doctor_files,
    #     "Result":pred
    # }
    # df = pd.DataFrame(df)
    # files = df.to_html(classes="table table-striped")
    if doctor_files:
        return render_template('doctor.html', files=message)
    
    else:
        return render_template('doctor.html', message=["Error: Failed to upload files"])

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')



if __name__ == '__main__':
    # To Run on Localhost, Uncomment the below line
    # app.run(debug=True, port=5500)

    # To Run on Network, Uncomment the below line
    app.run(host=socket.gethostbyname(socket.gethostname()), debug=True, port=5500)