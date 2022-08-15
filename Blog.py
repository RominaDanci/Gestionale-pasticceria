from flask import Blueprint, render_template, url_for, flash, request
from flask_login import current_user
from werkzeug.utils import redirect

from Utility import Auxcarrello, pages, help
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerRangeField, \
    validators, TimeField, TextAreaField, FloatField, FieldList, Form, FormField, IntegerField, DateField, \
    PasswordField, TelField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from GenDB import *


blog = Blueprint('blog', __name__)

class FormAddArticolo(FlaskForm):
    Titolo = StringField(validators=[InputRequired()], render_kw={"placeholder": "Titolo"})
    Contenuto = TextAreaField(validators=[InputRequired()], render_kw={"placeholder": "Scrivi qui..."})
    Categoria = StringField(validators=[InputRequired()], render_kw={"placeholder": "Categoria"})

    submit = SubmitField('Pubblica')


@blog.route('/blog')
def blogRoute():
    pages.disattiva(2)
    articoli = Articoli.query.order_by(Articoli.DataPubblicazione).all()
    autori = Blog.query.join(Articoli).filter(Articoli.Id == Blog.Id_Articolo).all()
    post = articoli[0]
    if current_user.is_authenticated:
        utente = current_user.Nome
    else:
        utente = ''

    return render_template("sito/blog.html", ID = post.Id, testo = post, total = Auxcarrello.quantità, totalMoney = Auxcarrello.totale, artic = list(articoli), len_artic = len(list(articoli)), aut = list(autori), len_aut = len(list(autori)), user = utente, pages = list(pages.pagine))

@blog.route('/blog-details/<id>')
def blogDetailsRoute(id):
    pages.disattiva(2)
    if current_user.is_authenticated:
        utente = current_user.Nome
    else:
        utente = ''

    articolo = Articoli.query.filter(Articoli.Id == id).first()
    dipendente = Dipendenti.query.join(Blog).filter(Blog.Id_Articolo == id).filter(Dipendenti.Mail == Blog.Mail_Dipendente).first()
    autore = Persone.query.filter(Persone.Mail == dipendente.Mail).first()

    return render_template("sito/blog-details.html", total = Auxcarrello.quantità, totalMoney = Auxcarrello.totale, user = utente, pages = list(pages.pagine), artic = articolo, aut = autore)

#gestionale
@blog.route('/gBlog')
def Gblog():
    artic = Articoli.query.all()

    if artic == None:
        flash("Non ci sono articoli pubblicati fin ora")
        return render_template("gestionale/blog.html", articoli=0)
    else:
        aut = session.query(Blog.Mail_Dipendente).order_by(Blog.Id_Articolo)
        return render_template("gestionale/blog.html", articoli = list(artic), autore = list(aut))

@blog.route('/gBlogaddArticolo', methods=['GET', 'POST'])
def addArticolo():
    form = FormAddArticolo()
    if form.validate_on_submit():
        new_artc = Articoli(Titolo=form.Titolo.data, Categoria=form.Categoria.data, Contenuto=form.Contenuto.data, DataPubblicazione=date.today())
        db.session.add(new_artc)
        db.session.commit()

        articolo = session.query(Articoli.Id).filter(Articoli.DataPubblicazione == date.today()).first()
        new_Blog = Blog(Id_Articolo=int(articolo[0]), Mail_Dipendente=current_user.Mail)
        db.session.add(new_Blog)
        db.session.commit()

        return redirect(url_for("blog.Gblog"))

    return render_template("gestionale/formArticolo.html", form=form)

@blog.route('/Messaggi', methods=['GET', 'POST'])
def messaggi():
    mes = list(Messaggi.query.all())
    if request.method == "POST":
        help.aggiorna(0, request.form["mex"])
        end = help.endSlied(0)
        start = end - 10
        #calcolare qui lo slide di mex con end e start
        return render_template("gestionale/messaggi.html", messaggi=mes[start:end])
    else:
        return render_template("gestionale/messaggi.html", messaggi=mes[0:10])
