from flask import Flask, url_for
from flask import request
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class sempf_moiveapp(db.Model):
    MovieID = db.Column(db.Integer, primary_key=True)
    Movie_name = db.Column(db.String(255))
    Movie_rating = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | Movie: {1} | Rating: {2} | First Name: {3} | Last Name:".format(self.MovieID, self.Movie_name, self.Movie_rating, self.first_name, self.last_name)


class MovieForm(FlaskForm):
    MovieID = IntegerField('MovieID:')
    Movie_name = StringField('Movie:', validators=[DataRequired()])
    Movie_rating = StringField('Rating:', validators=[DataRequired()])
    first_name = StringField('Lead Actor/Actress First Name:', validators=[DataRequired()])
    last_name = StringField('Lead Actor/Actress Last Name:', validators=[DataRequired()])


@app.route('/')
def index():
    all_movies = sempf_moiveapp.query.all()
    return render_template('index.html', movies = all_movies, pageTitle="Noah's Movie Ratings")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = sempf_moiveapp.query.filter(sempf_moiveapp.Movie_name.like(search)).all()
        return render_template('index.html', movies=results, pageTitle='Noah\'s Movie Ratings', legend="Search Results")
    else:
        return redirect('/')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        Movie = sempf_moiveapp(Movie_name=form.Movie_name.data, Movie_rating=form.Movie_rating.data, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(Movie)
        db.session.commit()

        return redirect('/')
 
    return render_template('add_movie.html', form=form, pageTitle='Add a new movie')

@app.route('/delete_movie/<int:MovieID>', methods=['GET','POST'])
def delete_movie(MovieID):
    if request.method == 'POST':
        Movie = sempf_moiveapp.query.get_or_404(MovieID)
        db.session.delete(Movie)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")


@app.route('/movie/<int:MovieID>', methods=['GET','POST'])
def get_movie(MovieID):
    Movie = sempf_moiveapp.query.get_or_404(MovieID)
    return render_template('movie.html', form=Movie, pageTitle='Movie Details', legend="Movie Details")


@app.route('/movie/<int:MovieID>/update', methods=['GET', 'POST'])
def update_movie(MovieID):
    Movie = sempf_moiveapp.query.get_or_404(MovieID)
    form = MovieForm()

    if form.validate_on_submit():
        Movie.Movie_name = form.Movie_name.data
        Movie.Movie_rating = form.Movie_rating.data
        Movie.first_name = form.first_name.data
        Movie.last_name = form.last_name.data
        db.session.commit()
        return redirect(url_for('get_movie', MovieID=Movie.MovieID))
    form.MovieID.data = Movie.MovieID
    form.Movie_name.data = Movie.Movie_name
    form.Movie_rating.data = Movie.Movie_rating
    form.first_name.data = Movie.first_name
    form.last_name.data = Movie.last_name
    return render_template('update_movie.html', form=form, pageTitle='Update Movie', legend="Update a movie")



if __name__ == '__main__':
    app.run(debug=True)
