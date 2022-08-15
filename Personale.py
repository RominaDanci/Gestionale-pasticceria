from datetime import date
from datetime import datetime
from sqlalchemy import func
from werkzeug.utils import redirect
from flask import Blueprint, render_template, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerRangeField, \
    validators, TimeField, TextAreaField, FloatField, FieldList, Form, FormField, IntegerField, DateField, \
    PasswordField, TelField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from GenDB import *

personale = Blueprint('personale', __name__)

class RegistrazioneDipendente(FlaskForm):
    nome = StringField(validators=[InputRequired()], render_kw={"placeholder": "Nome"})
    cognome = StringField(validators=[InputRequired()], render_kw={"placeholder": "Cognome"})
    datanascita = DateField(validators=[InputRequired()], format='%Y-%m-%d')
    mail = StringField(validators=[InputRequired()], render_kw={"placeholder": "Mail"})
    #username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    #password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    #password_confirm = PasswordField(validators=[InputRequired(), EqualTo('password', message='Passwords must match')],render_kw={"placeholder": "Repeat Password"})
    telefono = TelField(validators=[InputRequired()], render_kw={"placeholder": "Telefono"})

    submit = SubmitField('Register')

class addTurno(FlaskForm):
    dipendente = SelectField('Dipendente', choices=[])
    turno = SelectField('Turno', choices=[])
    data = DateField('Data')

    submit = SubmitField('Aggiungi')

@personale.route('/personaleGestionale')
def personaleGestionale():
    dip_data = session.query(Dipendenti.DataAssunzione).all()
    dip = Persone.query.join(Dipendenti).filter(Dipendenti.Mail == Persone.Mail).all()

    if dip == None:
        flash("Non hai dipendenti")
        return render_template("gestionale/dipendenti.html", len_Dip=0)


    return render_template("gestionale/dipendenti.html", Dip=list(dip), len_Dip=len(list(dip)), Dip_Data=list(dip_data), len_Dip_Data=len(list(dip_data)))

@personale.route('/aggiungiDipendente', methods=['GET', 'POST'])
def addDipendente():
    form = RegistrazioneDipendente()

    if form.validate_on_submit():
        new_Person = Persone(Nome=form.nome.data, Cognome=form.cognome.data, DataNascita=form.datanascita.data, Mail=form.mail.data, Telefono=form.telefono.data, Username='', Password='-', Rating=0)
        new_Dip = Dipendenti(Mail=form.mail.data, DataAssunzione=date.today())
        db.session.add(new_Person)
        db.session.add(new_Dip)
        db.session.commit()

    return render_template("gestionale/formDipendente.html", form=form)

@personale.route('/organizzazioneStaff', methods=['GET', 'POST'])
def organizzazioneStaffGestionale():
    personale = session.query(PersonaleTurni.Data, PersonaleTurni.Mail_Dipendente, Turni.Nome, Turni.OraInizioTurno, Turni.OraFineTurno)\
        .join(Turni, Turni.Id == PersonaleTurni.Id_Turno).all()

    events = []

    for x in personale:
        events.append({
            'Dipendente' : x.Mail_Dipendente,
            'Turno' : x.Nome,
            'Data' : x.Data,
            'OraInizio' : x.OraInizioTurno,
            'OraFine' : x.OraFineTurno,
        })

    return render_template("gestionale/organizzazioneStaff.html", events = events)

@personale.route('/addDipTurno', methods=['GET', 'POST'])
def addDipendenteTurno():
    form = addTurno()
    form.dipendente.choices = [ dipendente.Nome + " " + dipendente.Cognome for dipendente in Persone.query.join(Dipendenti).filter(Persone.Mail == Dipendenti.Mail).all()]
    form.turno.choices = [turno.Nome for turno in Turni.query.all()]

    if request.method == 'POST':
        dip = form.dipendente.data.split()

        dipMail = session.query(Persone.Mail).filter(Persone.Nome == dip[0]).filter(Persone.Cognome == dip[1]).first()
        turnoId = session.query(Turni.Id).filter(Turni.Nome == form.turno.data).first()

        oraI = session.query(Turni.OraInizioTurno).filter(Turni.Id == turnoId[0]).first()
        oraF = session.query(Turni.OraFineTurno).filter(Turni.Id == turnoId[0]).first()

        new_persTurni = PersonaleTurni(Mail_Dipendente = dipMail[0], Id_Turno = turnoId[0], OraInizio = str(oraI[0]), OraFine = str(oraF[0]), Data=form.data.data)
        db.session.add(new_persTurni)
        db.session.commit()

        return redirect(url_for("personale.organizzazioneStaffGestionale"))


    return render_template("gestionale/formTurno.html", form=form)

@personale.route('/turni/<id>')
def tabellaTurni(id):
    turni = list(session.query(Turni.Nome, Turni.CompensoOrario, Turni.OraInizioTurno, Turni.OraFineTurno, PersonaleTurni.OraInizio, PersonaleTurni.OraFine).join(PersonaleTurni).filter(PersonaleTurni.Mail_Dipendente == id).filter(PersonaleTurni.Id_Turno == Turni.Id).order_by(PersonaleTurni.Id_Turno))
    dip = Persone.query.filter(Persone.Mail == id).first()

    differenze = []

    for x in turni:
        dateTimeA = datetime.combine(date.today(), x.OraInizio)
        dateTimeB = datetime.combine(date.today(), x.OraFine)
        # Get the difference between datetimes (as timedelta)
        dateTimeDifferenceAll = dateTimeB - dateTimeA

        dateTimeA = datetime.combine(date.today(), x.OraInizioTurno)
        dateTimeB = datetime.combine(date.today(), x.OraFineTurno)
        dateTimeDifference = dateTimeB - dateTimeA

        y = (dateTimeDifference.total_seconds()/3600, (dateTimeDifferenceAll-dateTimeDifference).total_seconds()/3600)

        differenze.append(y)

    tot = 0
    totStra = 0

    for x in differenze:
        tot+=x[0]
        totStra+=x[1]

    if len(turni) > 0:
        stipendio = (tot * turni[0].CompensoOrario) + (totStra * (turni[0].CompensoOrario + 1.5))
    else:
        stipendio =0
    data = str(datetime.now().month) + "/" + str(datetime.now().year)

    return render_template("gestionale/turniSingle.html", Dip=dip, meseACT=data, Turni = turni, Differenze = differenze, TotOre=tot, TotOreStra=totStra, Stip=round(stipendio, 2))

