import os
from flask import Flask, render_template, request, redirect
from zeep import Client

app = Flask(__name__)
SOAP_URL = os.environ.get('SOAP_URL', 'http://soap_server:8000/soap?wsdl')
client = Client(SOAP_URL)

@app.route('/')
def index():
    persons = client.service.get_all_person()
    return render_template('index.html', persons=persons)

@app.route('/add_person', methods=['POST'])
def add_person():
    name = request.form['name']
    birth_date = request.form['birth_date']  # yyyy-mm-dd
    client.service.add_person(name, birth_date)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
