from flask import Flask, render_template, request, redirect
from zeep import Client

app = Flask(__name__)
SOAP_URL = 'http://localhost:8000/soap'
client = Client(SOAP_URL)

@app.route('/')
def index():
    persons = client.service.get_all_persons()
    return render_template('index.html', persons=persons)

@app.route('/add_person', methods=['POST'])
def add_person():
    name = request.form['name']
    birth_date = request.form['birth_date']  # yyyy-mm-dd
    client.service.add_person(name, birth_date)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=5000)
