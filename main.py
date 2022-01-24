from flask import Flask, render_template, request, flash
from data import calculate

app = Flask(__name__)

app.config['SECRET_KEY'] = 's3cr3t'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def indexP():
    plasticProduced = request.form.get('plasticproduced')
    wastePerPerson = request.form.get('wasteperperson')
    population = request.form.get('population')

    print(wastePerPerson.isdigit())

    try:
        predictedValue = calculate(float(plasticProduced), float(wastePerPerson), float(population))
        flash('Your country will contribute to ' + str(round(predictedValue[0], 2)) + ' percent of global waste', 'success')
        return render_template('index.html')
    except:
        flash('Invalid input. Input must consist of integers or decimals.', 'error')
        return render_template('index.html')