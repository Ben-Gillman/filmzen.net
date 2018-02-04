from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
import movie_recommendation_engine as movrec
import movie_scraping as movscrp
import movie_caching as movcache
from config import Config
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class MovieForm(FlaskForm):
    movieName = StringField(label='Enter a movie:', 
                       validators=[Required(), Length(1, 50)])
    submitMovie = SubmitField(label='Find Movies')

class FeedbackForm(FlaskForm):
    feedbackText = StringField(label='Happy with your recommendations? Not happy? Tell us about it!', 
                       validators=[Required(), Length(1, 280)])
    submitFeedback = SubmitField(label='Submit Review')

class UserInput(db.Model):
    __tablename__ = 'user_input'
    id = db.Column(db.Integer, primary_key=True)
    likedMovie = db.Column(db.String(50), index=True, unique=False)


class UserFeedback(db.Model):
    __tablename__ = 'user_feedback'
    id = db.Column(db.Integer, primary_key=True)
    likedMovie = db.Column(db.String(50), index=True, unique=False) 
    feedback = db.Column(db.String(280), index=True, unique=False)


@app.route('/', methods = ['GET', 'POST'])
def movie():
    movie_name = None
    print_movie_name = None
    movie_form = MovieForm()
    movie_count = 0
    top_movies = movcache.get_empty_cache()
    feedback_form = FeedbackForm()

    if movie_form.submitMovie.data and movie_form.validate():
        movie_name = movie_form.movieName.data
        movie_form.movieName.data = ''
        movie_count = UserInput.query.filter_by(likedMovie=movie_name).count()

        movie_id = movrec.get_movie_id(movie_name, db.get_engine())
        if movie_id == -1:
            return render_template('movie.html', form=movie_form, error=True)

        print_movie_name = movrec.get_print_movie_name(movie_id, db.get_engine())
        session['likedMovie'] = print_movie_name
        top_movies = movcache.return_cache_result(movie_id, db.get_engine())

        db.session.add(UserInput(likedMovie=print_movie_name))
        db.session.commit()

        if (top_movies.empty or top_movies.iloc[0,0] == 0):
            print("INFO: calculating new scores")
            liked_rated = movrec.rating_similarity(movie_id, db.get_engine())
            genome_similarity = movrec.get_genomes(movie_id, db.get_engine())
            top_movies = movrec.calculate_scores(liked_rated, genome_similarity, db.get_engine())
            if len(top_movies) < 3:
                return render_template('movie.html', movie1=0, form=movie_form, 
                                        name=print_movie_name, error=True, count=session['count'])
            top1, top2, top3 = top_movies.iloc[0,2], top_movies.iloc[1,2], top_movies.iloc[2,2]
            imdb_media = movscrp.get_media_links(top_movies['imdbId'])
            top_movies = pd.concat([top_movies, imdb_media], axis=1)
            top_movies = top_movies.drop('index', 1)
            movcache.cache_result(top_movies, db.get_engine())

    if 'count' not in session:
        session['count'] = 1
    else:
        session['count'] += 1  

    if feedback_form.submitFeedback.data and feedback_form.validate():
        feedback_text = feedback_form.feedbackText.data
        feedback_form.feedbackText.data = ''
        db.session.add(UserFeedback(likedMovie=session.get('likedMovie', None), feedback=feedback_text))
        db.session.commit()


    return render_template('movie.html', movieForm=movie_form, feedbackForm=feedback_form, likedMovie=print_movie_name, count=session['count'],
                            movie_count=movie_count, 
                            movie1=top_movies.iloc[0,2], movie2=top_movies.iloc[1,2], movie3=top_movies.iloc[2,2], 
                            link1=top_movies.iloc[0,3], link2=top_movies.iloc[1,3], link3=top_movies.iloc[2,3], 
                            poster1=top_movies.iloc[0,5], poster2=top_movies.iloc[1,5], poster3=top_movies.iloc[2,5],
                            trailer1=top_movies.iloc[0,6], trailer2=top_movies.iloc[1,6], trailer3=top_movies.iloc[2,6],
                            description1=top_movies.iloc[0,7], description2=top_movies.iloc[1,7], description3=top_movies.iloc[2,7])


@app.route('/about/')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404_error.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)