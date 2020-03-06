from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class sempf_ratingapp(db.Model):
    MovieID = db.Column(db.Integer, primary_key=True)
    Movie_name = db.Column(db.String(255))
    Movie_rating = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | Movie: {1} | Rating: {2} | First Name: {3} | Last Name:".format(self.MovieID, self.Movie_name, self.Movie_rating, self.first_name, self.last_name)


class MovieForm(FlaskForm):
    Movie_name = StringField('Movie:', validators=[DataRequired()])
    Movie_rating = StringField('Rating:', validators=[DataRequired()])
    first_name = StringField('Lead Actor/Actress First Name:', validators=[DataRequired()])
    last_name = StringField('Lead Actor/Actress Last Name:', validators=[DataRequired()])


@app.route('/')
def index():
    all_movies = sempf_ratingapp.query.all()
    return render_template('index.html', movies = all_movies, pageTitle="Noah's Movie Ratings")

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        Movie = sempf_ratingapp(Movie_name=form.Movie_name.data, Movie_rating=form.Movie_rating.data, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(Movie)
        db.session.commit()

        return "<h2> The movie {0} stars {1} {2} and I would rate it a {3}".format(form.Movie_name.data, form.first_name.data, form.last_name.data, form.Movie_rating.data)
 
    return render_template('add_movie.html', form=form, pageTitle='Add a new movie') 

if __name__ == '__main__':
    app.run(debug=True)
