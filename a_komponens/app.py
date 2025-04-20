import os
from flask import Flask, render_template, request, redirect
from zeep import Client

app = Flask(__name__, template_folder='templates', static_folder='static')
SOAP_URL = os.environ.get('SOAP_URL', 'http://soap_server:8000/soap?wsdl')
client = Client(SOAP_URL)

@app.route('/')
def index():
    persons = client.service.get_all_person()
    return render_template('index.html', persons=persons)

@app.route('/add_person', methods=['POST'])
def add_person():
    name = request.form['nev']
    birth_date = request.form['szul_ido']
    birth_place = request.form['szul_hely']
    mother_name = request.form['anyja_neve']
    gender = request.form['nem']
    address = request.form['lakcim']
    email = request.form['email']
    client.service.add_person(name, birth_date, birth_place, mother_name, gender, address, email)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
