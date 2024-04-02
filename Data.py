import pandas as pd

class Dataset:
    dataset = {
        'Name': [],
        'Age': [],
        'Gender': [],
        'contact': [],
        'file_name': [],
        'result' : []
    }

    def __init__(self, name, age, gender, contact, file_name, result):
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact
        self.file_name = file_name
        self.result = result
        # self.dataset['Name'].append(name)
        # self.dataset['Age'].append(age)
        # self.dataset['Gender'].append(gender)
        # self.dataset['contact'].append(contact)
        # self.dataset['file_name'].append(file_name)
        self.df = pd.DataFrame(self.dataset)

    def add(self, name='', age='', gender='', contact='', file_name='', result =''):
        self.dataset['Name'].append(name)
        self.dataset['Age'].append(age)
        self.dataset['Gender'].append(gender)
        self.dataset['contact'].append(contact)
        self.dataset['file_name'].append(file_name)
        self.dataset['result'].append(result)
        self.df = pd.DataFrame(self.dataset)
        return self  # Return self to enable method chaining

    def save(self):
        if not self.df.empty:
            excel_path = 'excel/patient.xlsx'
            self.df.to_excel(excel_path, index=False)
            print('Data saved successfully')
        else:
            print('No data to save')

def Doctor(files,reports, rate):
    data ={
        'files_name' : [],
        'reports':[],
    }
    for i in range(len(files)):
        data['files_name'].append(files[i])
        data['reports'].append(reports[i])
    df =pd.DataFrame(data)
    excel_path = 'excel/doctor.xlsx'
    if not df.empty:
        df = df.sort_values('reports',ascending=False)
        df.to_excel(excel_path,index=False)

        print('Data  Saved')
    else:
        print('Data Not Saved')