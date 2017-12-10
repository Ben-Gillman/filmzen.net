from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
import movie_recommendation_engine as movrec

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class MovieForm(FlaskForm):
    name = StringField(label='What is your favorite movie?', 
                             validators=[Required(), Length(1, 50)])
    submit = SubmitField('Submit')


class UserInput(db.Model):
    __tablename__ = 'user_input'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=False)

    # def __repr__(self):
    #     return '<Movie: {0}>'.format(self.name)


class MovieMaster(db.Model):
    __tablename__ = 'movie_master'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=False)



@app.route('/', methods = ['GET', 'POST'])
def index():
    movie_name = None
    movie_form = MovieForm()
    prev_like = None
    movie_count = 0
    top1 = None
    top2 = None
    top3 = None

    if movie_form.validate_on_submit(): #Becomes true when user pushes button
        movie_name = movie_form.name.data
        movie_form.name.data = ''
        movie_count = UserInput.query.filter_by(name=movie_name).count()
        if movie_count > 0:
            prev_like = 1
        db.session.add(UserInput(name=movie_name))
        db.session.commit()

        movie_id = movrec.get_movie_id(movie_name, db.get_engine())
        liked_rated = movrec.rating_similarity(movie_id, db.get_engine())
        genome_similarity = movrec.get_genomes(movie_id, db.get_engine())
        top_list = movrec.calculate_scores(liked_rated, genome_similarity, db.get_engine())
        top1 = top_list[0]
        top2 = top_list[1]
        top3 = top_list[2]

    if 'count' not in session:
        session['count'] = 1
    else:
        session['count'] += 1

    # return render_template('index.html', form=movie_form, 
    #                         name=movie_name, count=session['count'],
    #                         prev_like=prev_like, movie_count=movie_count)    

    return render_template('movie.html', form=movie_form, name=movie_name, count=session['count'],
                            prev_like=prev_like, movie_count=movie_count, movie1 = top1, 
                            movie2 = top2, movie3 = top3)

@app.route('/movie-recs/')
def movie_recs():
    return render_template('movie_recs.html')


@app.route('/the-future/')
def the_future():
    return render_template('the_future.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404_error.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)