import os 
import subprocess 
import json
import datetime

#create .env first!
with open('latrom/settings/.env', 'w') as f:
    secret_key = input('enter sercret key') 
    email_key = input('enter email key')
    f.write(f"SECRET_KEY='{secret_key}'")
    f.write(f"EMAIL_KEY='{email_key}'")

with open('database/config.json', 'w') as f:
    json.dump({'current': 'db.sqlite3'}, f)

with open('license.json', 'w') as f:
    customer = input('enter customer name: ')
    employees = input('enter number employees: ')
    users = input('enter number users: ')
    length = input('enter the length of validity: ')
    

    json.dump({'license': {
        "customer": customer,
        "number_users": users,
        "number_employees": employees,
        "date_issued": datetime.date.today().strftime('%d/%m/%Y'),
        "expiry_date": (datetime.date.today() + \
             datetime.timedelta(days=int(length))).strftime('%d/%m/%Y'),
        "timestamp": datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    }}, f)

subprocess.run('mkvirtualenv env --python=/usr/bin/python3.6'.split(' '))
subprocess.run('pip install -r requirements.txt'.split(' '))




subprocess.run('python manage.py makemigrations'.split(' '))
subprocess.run('python manage.py migrate'.split(' '))
subprocess.run('python manage.py collectstatic --no-input'.split(' '))


#manually configure .env file with the following code
#SECRET_KEY=''
#EMAIL_KEY=''