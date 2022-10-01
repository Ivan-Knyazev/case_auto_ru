import os
import time
import locale
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from network_2 import result_for_network

# from flask_ngrok import run_with_ngrok

UPLOAD_FOLDER = '/home/ivan/PycharmProjects/server_ml/fotos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# run_with_ngrok(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bodyType = db.Column(db.String(20), nullable=False)
    brand = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    # ---------
    enginePower = db.Column(db.Integer, nullable=False)
    # ---------
    fuelType = db.Column(db.String(20), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    model_info = db.Column(db.String(30), nullable=False)
    numberOfDoors = db.Column(db.Integer, nullable=False)
    vehicleTransmission = db.Column(db.String(30), nullable=False)
    owners = db.Column(db.Integer, nullable=False)
    vehicle_passport = db.Column(db.String(15), nullable=False)
    type_of_drive = db.Column(db.String(15), nullable=False)
    wheel = db.Column(db.String(15), nullable=False)

    modelDate = db.Column(db.Integer, nullable=False)
    productionDate = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    engineDisplacement = db.Column(db.String(15), nullable=False)  # Float
    # price = db.Column(db.Integer)
    date = db.Column(db.Integer, default=int(time.time()))


def is_float(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/create_car', methods=['POST'])
def create_car():
    # if request.method == "POST":
    data = dict(request.form)
    print(data)

    if int(data['productionDate']) - int(data['modelDate']) < 0:
        error = 'Неверно указаны год выпуска и год поступления модели в продажу!'
        return render_template('mistake.html', error=error)

    if is_float(data['engineDisplacement']) == False:
        error = 'Неверно указан объём двигателя!'
        return render_template('mistake.html', error=error)

    if int(data['numberOfDoors']) > 5:
        error = 'Неверно указано кол-во дверей!'
        return render_template('mistake.html', error=error)

    try:
        engineDisplacement = str(float(data['engineDisplacement'])) + ' LTR'
        print(engineDisplacement)
        car = Data(bodyType=str(data['bodyType']), brand=str(data['brand']), color=str(data['color']),
                   description=str(data['description']), enginePower=int(data['enginePower']),
                   fuelType=str(data['fuelType']),
                   mileage=int(data['mileage']), model_info=str(data['model_info']),
                   numberOfDoors=int(data['numberOfDoors']),
                   vehicleTransmission=str(data['vehicleTransmission']), owners=int(data['owners']),
                   vehicle_passport=str(data['vehicle_passport']),
                   type_of_drive=str(data['type_of_drive']), wheel=str(data['wheel']),
                   modelDate=int(data['modelDate']), productionDate=int(data['productionDate']),
                   name=str(data['name']), engineDisplacement=engineDisplacement)
        db.session.add(car)
        # db.session.flush()
        db.session.commit()
        print('Добавление в БД успешно завершено!')
    except Exception as e:
        db.session.rollback()
        error = 'Ошибка добавления в БД'
        print(error)
        print(e)
        return render_template("mistake.html", error=error)

    result = round(result_for_network() * 1.4)
    # res = number(result)
    # res = format(result, ".")

    locale.setlocale(locale.LC_ALL, '')
    # res = locale.format('%d', result, grouping=True)
    res = locale.format_string('%d', result, grouping=True)
    print(res)

    return render_template("thanks.html", result=res,
                           bodyType=str(data['bodyType']), brand=str(data['brand']), color=str(data['color']),
                           description=str(data['description']), enginePower=int(data['enginePower']),
                           fuelType=str(data['fuelType']),
                           mileage=int(data['mileage']), model_info=str(data['model_info']),
                           numberOfDoors=int(data['numberOfDoors']),
                           vehicleTransmission=str(data['vehicleTransmission']), owners=int(data['owners']),
                           vehicle_passport=str(data['vehicle_passport']),
                           type_of_drive=str(data['type_of_drive']), wheel=str(data['wheel']),
                           modelDate=int(data['modelDate']), productionDate=int(data['productionDate']),
                           name=str(data['name']), engineDisplacement=engineDisplacement
                           )


@app.route('/create_car_foto', methods=['POST'])
def create_car_foto():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['image'], filename))


if __name__ == '__main__':
    # from waitress import serve
    app.run(host='0.0.0.0', port=8000, debug=True)
    # app.run()
