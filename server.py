import json, importlib
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def load_clubs():
    with open('clubs.json') as c:
         list_of_clubs = json.load(c)['clubs']
         return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
         list_of_competitions = json.load(comps)['competitions']
         return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    club_names = []
    for club in clubs:
        club_names.append(club['name'])

    club_mail = []
    for club in clubs:
        club_mail.append(club['email'])

    club_points = []
    for club in clubs:
        club_points.append(club['points'])
    return render_template('index.html', club_names=club_names,
                           club_mail=club_mail, club_points=club_points,
                           len=len(club_names))


@app.route('/show_summary',methods=['POST'])
def show_summary():
    try:
        club = [club for club in clubs if club['email'] == request.form
        ['email']][0]
    except IndexError:
        flash('Sorry, that email wasnt found.')
        return redirect('/')
    return render_template('welcome.html',club=club,
                           competitions=competitions)


@app.route('/create_tournaments',methods=['get', 'post'])
def create_tournaments():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        number_of_places = request.form['numberOfPlaces']
        competition = {
            "name": name,
            "date": date,
            "numberOfPlaces": number_of_places
        }
        with open('competitions.json', 'r+') as file:
            data = json.load(file)
            data["competitions"].append(competition)
            file.seek(0)
            json.dump(data, file, indent=4)
        flash('Great-tournament create !')
        return render_template('tournaments.html')
    else:
        return render_template('tournaments.html')


@app.route('/book/<competition>/<club>')
def book(competition,club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] ==
                         competition][0]
    if found_club and found_competition:
        return render_template('booking.html',club=found_club,
                               competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=competitions)


@app.route('/purchase_places',methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] ==
                   request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    number_of_places = int(competition['numberOfPlaces'])
    places_required = int(request.form['places'])
    date = competition['date']
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if date < today:
        flash('Competition already done')
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    if places_required > 12:
        flash("you cannot book more than 12")
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    if places_required > int(club['points']) or places_required < 0:
        flash('Not enough points')
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    if places_required > number_of_places:
        flash('You cannot take more places than is available')
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    else:
        competition['numberOfPlaces'] =\
            int(competition['numberOfPlaces']) - places_required
        club['points'] = int(club['points']) - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club,
                               competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))