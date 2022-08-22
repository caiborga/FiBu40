from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import re
import functions

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Buchung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, unique=False, nullable=False)
    zahlungseingang = db.Column(db.DateTime, unique=False, nullable=True)
    rechnungsdatum = db.Column(db.DateTime, unique=False, nullable=False)
    brutto = db.Column(db.Float, unique=False, nullable=False)
    ust_key = db.Column(db.Integer, unique=False, nullable=False)
    belegnummer = db.Column(db.String, unique=False, nullable=False)
    buchungstext = db.Column(db.String, unique=False, nullable=False)
    kst = db.Column(db.Integer, unique=False, nullable=True)
    interne_belegnummer = db.Column(db.String, unique=True, nullable=False)
    pos_bezeichnung = db.Column(db.String, unique=False, nullable=False)
    netto = db.Column(db.Float, unique=False, nullable=False)
    ust = db.Column(db.Float, unique=False, nullable=False)
    
    # repr method repersents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"""
        position: {self.position}, 
        rechnungsdatum: {self.rechnungsdatum}, 
        zahlungseingang: {self.zahlungseingang},
        brutto: {self.brutto},
        ust-schlüssel: {self.ust_key},
        belegnummer: {self.belegnummer},
        vst-schlüssel: {self.vst_key},
        buchungstext: {self.buchungstext},
        auslage: {self.verauslagt},
        kst: {self.kst}, 
        interne belegnummer: {self.interne_belegnummer},
        position bezeichnung: {self.pos_bezeichnung},
        netto: {self.netto}, 
        ust: {self.ust}
        """

class Positionen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, unique=True, nullable=False)
    bezeichnung = db.Column(db.String, unique=False, nullable=False)
    einaus = db.Column(db.Integer, unique=False, nullable=False)
    kategorie = db.Column(db.Integer, unique=False, nullable=True)

    def __repr__(self):
        return f"""
        position: {self.position}, 
        bezeichnung: {self.bezeichnung},
        einaus: {self.einaus},
        kategorie: {self.kategorie}
        """

class UstKeys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True, nullable=False)
    ust = db.Column(db.Integer, unique=False, nullable=False)
    bezeichnung = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return f"""
        code: {self.code}, 
        ust: {self.ust}
        bezeichnung: {self.bezeichnung}
        """

def int_belegnummer(rechnungsdatum):
    descending = Buchung.query.order_by(Buchung.id.desc())
    try:
        last_item_Buchung = descending.first().id
    except: 
        last_item_Buchung = 0
    return str(rechnungsdatum.year) + '-' + str(rechnungsdatum.month) + '-' +  str(last_item_Buchung+1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buchungen/<fehlercode>')
def check(fehlercode):
    buchungen = Buchung.query.all()
    positionen = Positionen.query.all()
    ustkeys = UstKeys.query.all()
    error = functions.get_error_buchungen(fehlercode)
    message = error['message']
    box = error['box']
    return render_template('buchungen.html', buchungen=buchungen, positionen = positionen, ustkeys=ustkeys, message=message, box=box)

@app.route('/add', methods=["POST"])
def add_buchung():

    position_dict = {}
    position_database = Positionen.query.all()
    for data in position_database:
        position_dict.update({data.position : data.bezeichnung})
    ust_dict = {}
    ust_database = UstKeys.query.all()
    for data in ust_database:
        ust_dict.update({data.code : data.ust})
  
    position = request.form.get("ilposition")
    rechnungsdatum = request.form.get("rechnungsdatum")
    zahlungseingang = request.form.get("zahlungseingang")
    brutto = request.form.get("brutto")
    ust_key = request.form.get("ilust")
    belegnummer = request.form.get("belegnummer")
    buchungstext = request.form.get("buchungstext")
    kst = request.form.get("kst")

    if position == '' or re.match("^\\d+$", position) == None:
        return redirect('/buchungen/2')
    else:
        if int(position) in position_dict:
            position = int(position)
        else:
            return redirect('/buchungen/3')

    if rechnungsdatum == '':
        return redirect('/buchungen/4')
    else:
        try:
            rechnungsdatum = datetime.strptime(rechnungsdatum, "%d.%m.%Y")
        except ValueError:
            return redirect('/buchungen/4')

    if zahlungseingang == '':
        zahlungseingang = None
    else:
        try:
            zahlungseingang = datetime.strptime(zahlungseingang, "%d.%m.%Y")
        except ValueError:
            return redirect('/buchungen/5')

    if brutto == '' or re.match("^[0-9]+(\.[0-9]{1,2})?$", brutto) == None:
        return redirect('/buchungen/6')
    else:
        brutto = float(brutto)

    if ust_key == '' or re.match("^\\d+$", ust_key) == None:
        return redirect('/buchungen/7')
    else:
        if int(ust_key) in ust_dict:
            ust_key = int(ust_key)
        else:
            return redirect('/buchungen/7')
 
    if kst == '' or re.match("^\\d+$", kst) == None:
        return redirect('/buchungen/9')
    else:
        kst = int(kst)

    interne_belegnummer = int_belegnummer(rechnungsdatum)
    pos_bezeichnung = position_dict[position]
    netto = brutto / (1 + (ust_dict[ust_key]/100))
    ust = brutto - (brutto / (1+ (ust_dict[ust_key] / 100)))

    p = Buchung(
        position=position,
        rechnungsdatum=rechnungsdatum, 
        zahlungseingang=zahlungseingang,
        brutto=brutto,
        ust_key=ust_key,
        belegnummer=belegnummer,
        buchungstext=buchungstext,
        kst=kst,
        interne_belegnummer = interne_belegnummer,
        pos_bezeichnung = pos_bezeichnung,
        netto = netto,
        ust = ust)
        
    db.session.add(p)
    db.session.commit()
    return redirect('/buchungen/1')

@app.route('/add_position', methods=["POST"])
def position():
    position = request.form.get("position")
    bezeichnung = request.form.get("position_bezeichnung")
    einaus = request.form.get("einaus")
    kategorie = request.form.get("kategorie")

    position_list = []
    position_database = Positionen.query.all()
    for pos in position_database:
        position_list.append(pos.position)

    if position == '' or re.match("^\\d+$", position) == None:
        return redirect('/config/2')
    else:
        if int(position) in position_list:
            return redirect('/config/9')
        else:
            position = int(position)

    if bezeichnung == '':
        return redirect('/config/3')

    einaus = int(einaus)

    p = Positionen(
        position=position,
        bezeichnung=bezeichnung,
        einaus=einaus,
        kategorie=kategorie)
        
    db.session.add(p)
    db.session.commit()
    return redirect('/config/1')

@app.route('/add_ust', methods=["POST"])
def ust():
    code = request.form.get("code")
    ust = request.form.get("ust")
    bezeichnung = request.form.get("ust_bezeichnung")

    ust_list = []
    ust_database = UstKeys.query.all()
    for ust_entry in ust_database:
        ust_list.append(ust_entry.code)

    if code == '' or re.match("^\\d+$", code) == None:
        return redirect('/config/4')
    else:
        if int(code) in ust_list:
            return redirect('/config/10')
        else:
            code = int(code)

    if ust == '' or re.match("^\\d+$", ust) == None:
        return redirect('/config/5')
    else:
        ust = int(ust)

    if bezeichnung == '':
        return redirect('/config/6')

    p = UstKeys(
        code=code,
        ust=ust,
        bezeichnung=bezeichnung)
        
    db.session.add(p)
    db.session.commit()
    return redirect('/config/1')

@app.route('/delete/<int:id>/<int:database>')
def erase(id, database):
    if database == 0:
        data = Buchung.query.get(id)
        goto = 0

        p = Buchung(
        position=data.position,
        rechnungsdatum=data.rechnungsdatum, 
        zahlungseingang=data.zahlungseingang,
        brutto=(data.brutto * -1),
        ust_key=data.ust_key,
        belegnummer=data.belegnummer,
        buchungstext="Stornobuchung zu " + data.interne_belegnummer,
        kst=data.kst,
        interne_belegnummer = int_belegnummer(data.rechnungsdatum),
        pos_bezeichnung = data.pos_bezeichnung,
        netto = (data.netto + -1),
        ust = (data.ust * -1))
        
        data.buchungstext = "Storniert durch Buchung " + int_belegnummer(data.rechnungsdatum)

        db.session.add(p)
        db.session.add(data)
        db.session.commit()

    if database == 1:
        data = Positionen.query.get(id)
        goto = 1
        db.session.delete(data)
        db.session.commit()
    if database == 2:
        data = UstKeys.query.get(id)
        goto = 1
        db.session.delete(data)
        db.session.commit()
    
    if goto == 0:
        return redirect('/buchungen/10')
    if goto == 1:
        return redirect('/config/7')

@app.route('/bwa', defaults={'year': '0', 'range': 0}) 
@app.route('/bwa/<year>/<range>')
def bwa(year, range):

    #default
    if year == '0':
        bis = datetime.now()
        year = bis.year
        von = datetime(year, 1, 1)
    
    #individual range
    if len(str(year))>4:
        von = datetime.strptime(year, '%Y-%m-%d')
        bis = datetime.strptime(range, '%Y-%m-%d')

    if len(str(year))==4:
        year = int(year)

    #month range / other ranges
    if range == "Q1":
        von = datetime(year, 1, 1)
        bis = datetime(year, 3, 31)
    if range == "Q2":
        von = datetime(year, 4, 1)
        bis = datetime(year, 6, 30)
    if range == "Q3":
        von = datetime(year, 7, 1)
        bis = datetime(year, 9, 30)
    if range == "Q4":
        von = datetime(year, 10, 1)
        bis = datetime(year, 12, 31)
    if range == "ytd":
        von = datetime(year, 1, 1)
        bis = datetime.now()   
    if range == "Januar":
        von = datetime(year, 1, 1)
        bis = datetime(year, 1, 31)
    if range == "Februar":
        von = datetime(year, 2, 1)
        bis = datetime(year, 2, 28)
    if range == "März":
        von = datetime(year, 3, 1)
        bis = datetime(year, 3, 31)
    if range == "April":
        von = datetime(year, 4, 1)
        bis = datetime(year, 4, 30)
    if range == "Mai":
        von = datetime(year, 5, 1)
        bis = datetime(year, 5, 31)
    if range == "Juni":
        von = datetime(year, 6, 1)
        bis = datetime(year, 6, 30)
    if range == "Juli":
        von = datetime(year, 7, 1)
        bis = datetime(year, 7, 31)
    if range == "August":
        von = datetime(year, 8, 1)
        bis = datetime(year, 1, 31)
    if range == "September":
        von = datetime(year, 9, 1)
        bis = datetime(year, 9, 30)
    if range == "Oktober":
        von = datetime(year, 10, 1)
        bis = datetime(year, 10, 31)
    if range == "November":
        von = datetime(year, 11, 1)
        bis = datetime(year, 11, 30)
    if range == "Dezember":
        von = datetime(year, 12, 1)
        bis = datetime(year, 12, 31)
       
    einnahmen = []
    ausgaben = []
    pos_einnahmen = Positionen.query.filter(Positionen.einaus == 1)
    pos_ausgaben =  Positionen.query.filter(Positionen.einaus == 0)
    summe_einnahmen = 0
    summe_ausgaben = 0
    now = datetime.now()
    aktuelles_jahr = now.year
    for position in pos_einnahmen:
        buchungen = Buchung.query.filter(Buchung.zahlungseingang>=von, Buchung.zahlungseingang<=bis, Buchung.position==position.position)
        saldo = 0
        for buchung in buchungen:
            saldo = saldo + buchung.netto
        summe_einnahmen = summe_einnahmen + saldo
        einnahmen.append([position.position, position.bezeichnung, saldo])

    for position in pos_ausgaben:
        buchungen = Buchung.query.filter(Buchung.zahlungseingang>=von, Buchung.zahlungseingang<=bis, Buchung.position==position.position)
        saldo = 0
        for buchung in buchungen:
            saldo = saldo + buchung.netto
        summe_ausgaben = summe_ausgaben + saldo
        ausgaben.append([position.position, position.bezeichnung, saldo])
    
    GewVerSumme = summe_einnahmen - summe_ausgaben
    if GewVerSumme >= 0:
        GewVerText = "Gewinn"
        box = "mbgreen"
    if GewVerSumme < 0:
        GewVerText = "Verlust"
        box = "mbred"

    return render_template('bwa.html', 
        einnahmen=einnahmen, 
        ausgaben=ausgaben, 
        summe_einnahmen=summe_einnahmen, 
        summe_ausgaben=summe_ausgaben, 
        von=von, 
        bis=bis,
        GewVerText=GewVerText,
        GewVerSumme=GewVerSumme,
        box=box,
        aktuelles_jahr=aktuelles_jahr
        )

@app.route('/edit/<int:id>', methods=["POST"])
def edit(id):

    old_entry = Buchung.query.filter(Buchung.id == id).first()

    position_dict = {}
    position_database = Positionen.query.all()
    for data in position_database:
        position_dict.update({data.position : data.bezeichnung})
    ust_dict = {}
    ust_database = UstKeys.query.all()
    for data in ust_database:
        ust_dict.update({data.code : data.ust})

    position = request.form.get("position")
    rechnungsdatum = request.form.get("rechnungsdatum")
    zahlungseingang = request.form.get("zahlungseingang")
    brutto = request.form.get("brutto")
    ust_key = request.form.get("ust_key")
    belegnummer = request.form.get("belegnummer")
    buchungstext = request.form.get("buchungstext")
    kst = request.form.get("kst")

    if position == '' or re.match("^\\d+$", position) == None:
        return redirect('/buchungen/2')
    else:
        if int(position) in position_dict:
            old_entry.position = int(position)
            position = int(position)
        else:
            return redirect('/buchungen/3')

    if rechnungsdatum == '':
        return redirect('/buchungen/4')
    else:
        try:
            old_entry.rechnungsdatum = datetime.strptime(rechnungsdatum, "%d.%m.%Y")
        except ValueError:
            return redirect('/buchungen/4')

    if zahlungseingang == '':
        old_entry.zahlungseingang = None
    else:
        try:
            old_entry.zahlungseingang = datetime.strptime(zahlungseingang, "%d.%m.%Y")
        except ValueError:
            return redirect('/buchungen/5')

    if brutto == '' or re.match("^[0-9]+(\.[0-9]{1,2})?$", brutto[:-2]) == None:
        return redirect('/buchungen/6')
    else:
        old_entry.brutto = float(brutto[:-2])
        brutto = float(brutto[:-2])

    if ust_key == '' or re.match("^\\d+$", ust_key) == None:
        return redirect('/buchungen/7')
    else:
        if int(ust_key) in ust_dict:
            old_entry.ust_key = int(ust_key)
            ust_key = int(ust_key)
        else:
            return redirect('/buchungen/7')

    if kst == '' or re.match("^\\d+$", kst) == None:
        return redirect('/buchungen/9')
    else:
        old_entry.kst = int(kst)
        kst = int(kst)

    old_entry.belegnummer = belegnummer
    old_entry.buchungstext = buchungstext
    old_entry.interne_belegnummer = old_entry.interne_belegnummer
    old_entry.pos_bezeichnung = position_dict[position]
    old_entry.netto = brutto / (1 + (ust_dict[ust_key]/100))
    old_entry.ust = brutto - (brutto / (1+ (ust_dict[ust_key] / 100)))
    
    db.session.add(old_entry)
    db.session.commit()
    return redirect('/buchungen/11')
    
@app.route('/updatebwa/', methods=["POST"])
def update():

    von = request.form.get("von")
    bis = request.form.get("bis")
    return redirect(url_for('bwa', year=von, range=bis))

@app.route('/config/<fehlercode>')
def config(fehlercode):
    positionen = Positionen.query.all()
    ust_keys = UstKeys.query.all()
    error = functions.get_error_config(fehlercode)
    message = error['message']
    box = error['box']
    return render_template('config.html', positionen=positionen, ust_keys=ust_keys, message=message, box = box)

@app.route('/offen/')
def offene_posten():
    summe = 0
    posten = []
    heute = datetime.today()
    pos_einnahmen = Positionen.query.filter(Positionen.einaus == 1)
    for position in pos_einnahmen:
        buchungen = Buchung.query.filter(Buchung.position==position.position, Buchung.zahlungseingang==None)
        for buchung in buchungen:
            due = heute - buchung.rechnungsdatum
            if due.days <= 10:
                color = "#99f7ab"
            if due.days > 10 and due.days <= 30:
                color = "#F1BF98"
            if due.days > 30:
                color = "#65334D"
            summe=summe+buchung.brutto
            posten.append([buchung.position, buchung.belegnummer, buchung.brutto, buchung.rechnungsdatum, buchung.buchungstext, due.days, color])
    if summe >0:
        box = "mbred"
    else:
        box = "mbgreen"
    return render_template('OP.html', posten=posten, summe=summe, box=box) 