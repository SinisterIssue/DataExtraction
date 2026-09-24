import PyPDF2
import requests
import tabula
import pandas as pd
import json
import hashlib
# from ..general_utility import get_hash_of_html
# from ..s3_upload import hash_check

def get_hash_of_html(html_string):
    hash_object = hashlib.md5(html_string.encode('utf-8'))
    hash_of_html = hash_object.hexdigest()
    return hash_of_html

def to_json(dictionary):
   hash_obj = json.dumps(dictionary)
   with open("dictionary.json", "w") as ts:
       ts.write(hash_obj)

def get_data(slug_name):
    data_list = []
    link = 'https://www.southsiouxcity.org/egov/documents/1511458752_8118.pdf'
    user_agent = "scrapping_script/1.0"
    headers = {'User-Agent': user_agent}
    r = requests.get(link, headers=headers, stream = True)
    try:
        with open("downloadedPdf.pdf", "wb") as fd:
            fd.write(r.content)
        file = open('downloadedPdf.pdf', 'rb') 
        fileReader = PyPDF2.PdfFileReader(file)

        pages = fileReader.numPages
        columns = ['Warrant', 'Entered Date', 'Race', 'Sex', 'Age', 'Name', 'Warrant Charge', 'Felony or Misdemeanor']
        dictionary = {}
        for col in columns:
            dictionary[col] = []

        for page in range(1, pages+1):
            try:
                df_ = tabula.read_pdf("downloadedPdf.pdf", pages = page)[0]
                df_.to_excel(f'example.xlsx', header=True, index=False)
                table = pd.read_excel('example.xlsx')
                if page==1:
                    table = table.drop(0, axis=0)
                
                table = table.fillna('')

                for row in range(len(table)):
                    if len(list(table.iloc[row]))==8:
                        list_ = list(table.iloc[row])
                        for i in range(len(columns)):
                            dictionary[columns[i]].append(list_[i])
            except:
                pass

        length = len(dictionary['Name'])
        traveledEntities = []
        for i in range(length):
            arrestWarrant = ''
            lastUpdatedAt = ''
            race = ''
            gender = ''
            age = ''
            name = ''
            charges = ''
            warrantType = ''
            data_dict = {}

            name = dictionary['Name'][i].strip()
            if ',' in name:
                t_n = name.split(',')
                name = t_n[1].strip() + " " + t_n[0].strip()
            name = name.title()
            
            warrantType = dictionary['Warrant'][i].strip()
            lastUpdatedAt = dictionary['Entered Date'][i].strip()
            race = dictionary['Race'][i].strip()
            gender = dictionary['Sex'][i].strip()
            if dictionary['Age'][i]!='':
                age = str(int(dictionary['Age'][i])).strip()
            arrestWarrant = dictionary['Felony or Misdemeanor'][i].strip()
            charges = dictionary['Warrant Charge'][i].strip()
            charges = charges.title()

            if race=='W':
                race = 'White'
            elif race=='B':
                race = 'Black'
            elif race=='I':
                race = 'Islander'
            else:
                race = ''

            if gender=='M':
                gender = 'Male'
            elif gender=='F':
                gender = 'Female'
            else:
                gender = ''

            if arrestWarrant=='M':
                arrestWarrant = 'Misdemeanor'
            elif arrestWarrant=='F':
                arrestWarrant = 'Felony'
            else:
                arrestWarrant = ''
            
            if lastUpdatedAt!='' and '/' in lastUpdatedAt:
                d = lastUpdatedAt.split('/')[1]
                m = lastUpdatedAt.split('/')[0]
                y = lastUpdatedAt.split('/')[2]
                lastUpdatedAt = f"{d}/{m}/{y}"
            
            if name.strip()!='' and [name, age] not in traveledEntities:
                traveledEntities.append([name, age])
                data_dict['fullName'] = name
                if gender.strip()!='':
                    data_dict['gender'] = gender
                if race.strip()!='':
                    data_dict['race'] = race
                if age.strip()!='':
                    data_dict['age'] = age
                if charges.strip()!='':
                    data_dict['charges'] = charges
                if arrestWarrant.strip()!='':
                    data_dict['arrestWarrant'] = arrestWarrant
                if warrantType.strip()!='':
                    data_dict['warrantType'] = warrantType
                if lastUpdatedAt.strip()!='':
                    data_dict['lastUpdatedAt'] = lastUpdatedAt
                data_dict['policeStation'] = 'South Sioux City Police Department'
                if charges.strip()!='':
                    if age.strip()!='':
                        if gender.strip()!='':
                            if race.strip()!='':
                                data_dict['summary'] = f"{data_dict['fullName']} is a {data_dict['age']} years old {data_dict['race']} {data_dict['gender']} with a warrant held by the {data_dict['policeStation']} for the charges of {data_dict['charges']}."
                            else:
                                data_dict['summary'] = f"{data_dict['fullName']} is a {data_dict['age']} years old {data_dict['gender']} with a held warrant by the {data_dict['policeStation']} for the charges of {data_dict['charges']}."
                        else:
                            data_dict['summary'] = f"{data_dict['fullName']} is a {data_dict['age']} years old person who has a warrant held by the {data_dict['policeStation']} for the charges of {data_dict['charges']}."
                    else:
                        data_dict['summary'] = f"{data_dict['fullName']} has a warrant held by the {data_dict['policeStation']} for the charges of {data_dict['charges']}."
                else:
                    data_dict['summary'] = f"{data_dict['fullName']} has a warrant held by the {data_dict['policeStation']}."
                data_list.append(data_dict)
    except:
        pass
    return data_list

if __name__ == "__main__":
   data_list = get_data('add-slug-here')
   to_json(data_list)