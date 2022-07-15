from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

import logging

from sqlalchemy import null

#Create Flask instance
app = Flask(__name__)

#Change Flask config
app.config.update(
    DEBUG = True,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
)

#Create sql instance
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)


#Configure database
class Buchung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, unique=False, nullable=False)
    zahlungseingang = db.Column(db.DateTime, unique=False, nullable=True)
    rechnungsdatum = db.Column(db.DateTime, unique=False, nullable=False)
    brutto = db.Column(db.Float, unique=False, nullable=False)
    ust_key = db.Column(db.Integer, unique=False, nullable=False)
    belegnummer = db.Column(db.String, unique=False, nullable=False)
    vst_key = db.Column(db.Integer, unique=False, nullable=False)
    buchungstext = db.Column(db.String, unique=False, nullable=False)
    verauslagt = db.Column(db.Boolean, unique=False, nullable=False, default=False)
  
    # repr method repersents how one object of this datatable
    # will look like
    def __repr__(self):
        result = ()
        result["position"] = {self.position}
        result["rechnungsdatun"] = {self.rechnungsdatum}
        result["zahlungseingang"] = {self.zahlungseingang}
        result["brutto"] = {self.brutto}
        result["ust-schlüssel"] = {self.ust_key}
        result["belegnummer"] = {self.belegnummer}
        result["vst-schlüssel"] = {self.vst_key}
        result["buchungstext"] = {self.buchungstext}
        result["auslage"] = {self.verauslagt}

        return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buchungen/<fehlercode>')
def check(fehlercode):
    buchungen = Buchung.query.all()
    message = ""
    box=""
    if fehlercode == '0':
        message = ""
        box = "messagebox0"
    if fehlercode == '1':
        message = "Buchungssatz wurde erstellt!"
        box = "messagebox1"
    if fehlercode == '2':
        message = "Eingaben fehlerhaft!"
        box = "messagebox2"

    return render_template('buchungen.html', buchungen=buchungen, message=message, box=box)

@app.route('/add', methods=["POST"])
def profile():

    def check_for_valid_entries():
        if (rechnungsdatum == ""):
            return False
        else:
            return True
            
      
    # In this funcion we will input data from the 
    # form page and store it in our database.
    # Remember that inside the get the name should
    # exactly be the same as that in the html
    # input fields
    position = request.form.get("position")
    rechnungsdatum = request.form.get("rechnungsdatum")
    zahlungseingang = request.form.get("zahlungseingang")
    brutto = request.form.get("brutto")
    ust_key = request.form.get("ust-key")
    belegnummer = request.form.get("belegnummer")
    vst_key = request.form.get("vst-key")
    buchungstext = request.form.get("buchungstext")
    auslage = request.form.get("auslage")

    # create an object of the Profile class of models
    # and store data as a row in our datatable
    if check_for_valid_entries():
        if zahlungseingang == '':
            zahlungseingang = null
        else:
            zahlungseingang = datetime.strptime(zahlungseingang, "%d.%m.%Y")

        p = Buchung(
        position=position,
        rechnungsdatum=datetime.strptime(rechnungsdatum, "%d.%m.%Y"), 
        zahlungseingang=zahlungseingang,
        brutto=brutto,
        ust_key=ust_key,
        belegnummer=belegnummer,
        vst_key=vst_key,
        buchungstext=buchungstext,
        verauslagt=bool(auslage))
        db.session.add(p)
        db.session.commit()
        return redirect('/buchungen/1')
    else:
        return redirect('/buchungen/2')