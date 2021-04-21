from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# главная форма сайта
class MainForm(FlaskForm):
    city = StringField('Введите название города (для точности можно указать двухбуквенное название страны, например "Лондон, UK")', validators=[DataRequired()])
    submit = SubmitField('Узнать погоду')


# форма кнопки на странице с прогнозом
class WeatherForm(FlaskForm):
    submit = SubmitField('Назад')
