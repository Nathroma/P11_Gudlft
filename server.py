import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions, 
            date=str(datetime.now()))
    except IndexError:
        return render_template('index.html', error_message = "Aucune adresse email correspondante !" )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition and foundCompetition['date'] >= str(datetime.now()):
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Une erreur est apparue, veuillez reessayer")
        return render_template('welcome.html', club=club, competitions=competitions,
            date=str(datetime.now()))


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    if not competition['name'] in club:
        club[competition['name']] = int(0)

    placesRequired = int(request.form['places'])

    if placesRequired > int(competition['numberOfPlaces']):
        flash("Il n'y a pas assez de places disponible pour cette compétition.")
    elif placesRequired + club[competition['name']] > 12:
        flash("Vous ne pouvez pas prendre plus de 12 places")
    elif int(club['points']) < placesRequired * 3:
        flash("Vous n'avez pas assez de points")
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-placesRequired*3
        club[competition['name']] = int(club[competition['name']])+placesRequired
        flash('Great-booking complete! Number of places purchased: ' + str(placesRequired))
    return render_template('welcome.html', club=club, competitions=competitions,
        date=str(datetime.now()))


@app.route('/display')
def club_display():
    return render_template('display.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))