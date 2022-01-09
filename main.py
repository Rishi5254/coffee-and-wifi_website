from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Length
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donz'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name',
                       validators=[DataRequired(), Length(min=3, max=20, message="cafe name must be in 3-20 words")])
    url = StringField('Cafe Url', validators=[DataRequired(), URL()])
    open = StringField('Opening Time e.g.9AM)',
                       validators=[DataRequired(), Length(min=3, max=7, message="Invalid Format")])
    close = StringField('Closing Time e.g.10:30PM',
                        validators=[DataRequired(), Length(min=3, max=7, message="Invalid Format")])
    coffee_rating = SelectField(u'Cafe Rating', choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'], validators=[DataRequired()])
    wifi_rating = SelectField(u'Wifi Strength Rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'], validators=[DataRequired()])
    power_rating = SelectField(u'Power Socket Availability',choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("true")
        data = [form.cafe.data, form.url.data, form.open.data, form.close.data,
                form.coffee_rating.data, form.wifi_rating.data,
                form.power_rating.data]

        with open('cafe-data.csv', mode='a', encoding='utf-8') as file:
            file_writer = csv.writer(file)
            file_writer.writerow(data)
            file.close()

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []

        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
        list_of_rows = [n for n in list_of_rows if len(n) == 7]
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
