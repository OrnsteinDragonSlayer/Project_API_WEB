from flask import Flask, render_template, redirect
from forms.main_form import MainForm, WeatherForm
from data.functions import request_current_weather, request_forecast
from data.functions import get_city_id
from data.cities import Cities
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# главная страница
@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    form = MainForm()
    if form.validate_on_submit():
        if type(get_city_id(form.city.data)) != int:
            return render_template('main_page.html', form=form,
                                   message='Неверно введено название города')
        db_sess = db_session.create_session()
        city = Cities(city=form.city.data)
        db_sess.add(city)
        db_sess.commit()
        return redirect('/weather')
    return render_template('main_page.html', form=form)


# страница с прогнозом погоды
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    form = WeatherForm()
    db_sess = db_session.create_session()
    city = db_sess.query(Cities).order_by(Cities.id.desc()).first()
    positions_one_day = request_current_weather(get_city_id(city.city))
    positions_days = request_forecast(get_city_id(city.city))
    db_sess.delete(city)
    db_sess.commit()
    if form.validate_on_submit():
        return redirect('/main_page')
    return render_template('weather.html', positions_one_day=positions_one_day,
                           positions_days=positions_days, form=form)


def main():
    db_session.global_init('db/cities.db')
    app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
