from flask import Flask,render_template,request,send_from_directory
from Data import Dataset,Doctor
from PIL import Image
from a import prediction
import socket
import pandas as pd

def style_df(df):
    df = df.reset_index(drop=True)
    return df.style \
        .set_properties(**{'background-color': 'white', 
                           'color': 'black', 
                           'border-color': 'black',
                           'font-size': '1.6rem',
                           'width':'80%',
                           'text-align':'center',
                           'margin':'0 1rem'}) \
        .set_table_styles([{'selector': 'thead',
                            'props': [('background-color', 'rgb(128,128,128,0.5)'),
                                      ('color', 'black'),
                                      ('border-color', 'white'),
                                      ('font-size','2rem')]},
                           {'selector': 'tbody tr:hover',
                            'props': [('background-color', 'skyblue')
                                      ]}])



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
    data = [name,age,gender,contact,file.filename,result]
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
    df = pd.DataFrame({"files":doctor_files,"Result":pred})
    df = df.sort_values('Result',ascending=False)
    df = style_df(df=df)
    files = df.to_html(classes="table table-stripped",sparse_index=False)
    if doctor_files:
        return render_template('doctor.html', files=files)
    
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