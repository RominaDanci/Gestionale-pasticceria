from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from werkzeug.utils import redirect
from GenDB import *
from Utility import Auxcarrello, pages

ecommerce = Blueprint('ecommerce', __name__)


@ecommerce.route('/shop', methods=['GET', 'POST'])
def shop():
    pages.disattiva(1)
    if current_user.is_authenticated:
        utente = current_user.Nome
        cart = session.query(func.sum(Carrello.QuantitàCarrello)).filter(
            Carrello.Mail_Cliente == current_user.Mail).first()
        tot = session.query(func.sum(Semilavorati.PrezzoUnitario * Carrello.QuantitàCarrello).label('totcar')).join(
            Carrello).filter(Carrello.Mail_Cliente == current_user.Mail).filter(
            Semilavorati.Id == Carrello.Id_Semilavorato)
        if cart[0] == None and tot[0].totcar == None:
            Auxcarrello.totale = 0
            Auxcarrello.quantità = 0
        else:
            Auxcarrello.totale = round(float(tot[0].totcar), 2)
            Auxcarrello.quantità = cart[0]
    else:
        utente = ''
        Auxcarrello.totale = 0
        Auxcarrello.quantità = 0

    if request.method == "POST":
        if(request.form['hidden'] == '2'):
            id = request.form['scelta']
            if id == '2':
                Prodotti = Semilavorati.query.order_by(Semilavorati.PrezzoUnitario).all()
            else:
                Prodotti = Semilavorati.query.order_by(Semilavorati.Nome).all()
        else:
            cat = request.form["cat"]
            if(cat == "all"):
                Prodotti = Semilavorati.query.order_by(Semilavorati.Nome).all()
            else:
                Prodotti = Semilavorati.query.order_by(Semilavorati.Nome).filter(Semilavorati.Categoria == cat)
    else:
        Prodotti = Semilavorati.query.order_by(Semilavorati.Nome).all()
    return render_template("sito/shop.html", total = Auxcarrello.quantità, totalMoney = Auxcarrello.totale, Prod = list(Prodotti), lenProd = len(list(Prodotti)), pages = list(pages.pagine), user = utente)

@ecommerce.route('/shop-details/<id>', methods=['GET', 'POST'])
def shop_details(id):
    pages.disattiva(1)
    if current_user.is_authenticated:
        utente = current_user.Nome
        Prodotto = Semilavorati.query.filter(Semilavorati.Id == id).first()
    else:
        utente = ''
        Prodotto = None
    if request.method == "POST":
        quantita = request.form['quantita']
        if Carrello.query.filter(Carrello.Mail_Cliente == current_user.Mail).filter(Carrello.Id_Semilavorato == id).first() == None:
            new_cartProd = Carrello(Mail_Cliente = current_user.Mail, Id_Semilavorato = id, QuantitàCarrello = quantita)
            db.session.add(new_cartProd)
            db.session.commit()
        else:
            if int(quantita) > 0:
                Carrello.query.filter(Carrello.Mail_Cliente == current_user.Mail).filter(Carrello.Id_Semilavorato == id).update({"QuantitàCarrello" : quantita})
            else:
                delete_prod = Carrello.query.filter(Carrello.Mail_Cliente == current_user.Mail).filter(Carrello.Id_Semilavorato == id)
                delete_prod.delete()

            db.session.commit()

        return redirect(url_for('ecommerce.shop'))
    else:
        return render_template("sito/shop-details.html", total = Auxcarrello.quantità, totalMoney = Auxcarrello.totale,
                               id = Prodotto.Id, nome = Prodotto.Nome, prezzo = Prodotto.PrezzoUnitario, incipit = "incipit", categoria = 'categoria', tags = 'tag', descrizione="Prodotto.Preparazione", user = utente, pages = list(pages.pagine))

@ecommerce.route('/shoping-cart', methods=['GET', 'POST'])
def shoping_cart():
    pages.disattiva(1)
    if current_user.is_authenticated:
        utente = current_user.Nome
        prod = Semilavorati.query.join(Carrello).filter(Carrello.Mail_Cliente == current_user.Mail).filter(Carrello.Id_Semilavorato == Semilavorati.Id).order_by(Carrello.Id_Semilavorato)
        cart = Carrello.query.filter(Carrello.Mail_Cliente == current_user.Mail).order_by(Carrello.Id_Semilavorato).all()
        tot = session.query(func.sum(Semilavorati.PrezzoUnitario * Carrello.QuantitàCarrello).label('totcar')).join(Carrello).filter(Carrello.Mail_Cliente == current_user.Mail).filter(Semilavorati.Id == Carrello.Id_Semilavorato)

        if Carrello.query.filter(Carrello.Mail_Cliente == current_user.Mail).first() != None:
            return render_template("sito/shoping-cart.html", total = Auxcarrello.quantità, totalMoney = Auxcarrello.totale,
                                   Prod = list(prod), lenProd = len(list(prod)), Cart = list(cart), user = utente, pages = list(pages.pagine), totale = round(float(tot[0].totcar),2))
        else:
            flash("Il tuo carrello è attualmente vuoto")
            return render_template("sito/shoping-cart.html", total = Auxcarrello.quantità, totalMoney = Auxcarrello.totale,
                                   Prod = list(prod), lenProd = len(list(prod)), Cart = list(cart), user = utente, pages = list(pages.pagine))
    else:
        return redirect(url_for('profile.login'))

@ecommerce.route('/checkout')
@login_required
def checkout():
    pages.disattiva(1)
    if current_user.is_authenticated:
        utente = current_user.Nome
    else:
        utente = ''

    if Carrello.query.count() > 0:
        delete_cart = Carrello.query.filter(Carrello.Mail_Cliente == current_user.Mail)
        delete_cart.delete()
        db.session.commit()

    Auxcarrello.totale = 0
    Auxcarrello.quantità = 0

    print('esplodo')

    flash("Pagamento avvenuto con successo")

    return redirect(url_for('home'))

@ecommerce.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    pages.disattiva(1)
    if current_user.is_authenticated:
        utente = current_user.Nome
        list_wishlist = Semilavorati.query.join(WishList).filter(WishList.Mail_Cliente == current_user.Mail).filter(WishList.Id_Semilavorato == Semilavorati.Id).all()
        if WishList.query.filter(WishList.Mail_Cliente == current_user.Mail).first() != None:
            return render_template("sito/wishlist.html", total = Auxcarrello.quantità, totalMoney = Auxcarrello.totale, product = list(list_wishlist), len_product = len(list(list_wishlist)), user = utente, pages = list(pages.pagine))
        else:
            flash("La tua WishList è attualmente vuota")
            return render_template("sito/wishlist.html", total=Auxcarrello.quantità, totalMoney=Auxcarrello.totale,
                                   product=list(list_wishlist), len_product=len(list(list_wishlist)), user=utente, pages = list(pages.pagine))
    else:
        return redirect(url_for('profile.login'))

@ecommerce.route('/modifyWishlist/<id>')
@login_required
def modifyWishlist(id):
    new_cartProd = Carrello(Mail_Cliente = current_user.Mail, Id_Semilavorato = id, QuantitàCarrello = 1)
    delete_wishProd = WishList.query.filter(WishList.Mail_Cliente == current_user.Mail).filter(WishList.Id_Semilavorato == id)
    db.session.add(new_cartProd)
    delete_wishProd.delete()
    db.session.commit()

    cart = session.query(func.sum(Carrello.QuantitàCarrello)).filter(Carrello.Mail_Cliente == current_user.Mail).first()
    tot = session.query(func.sum(Semilavorati.PrezzoUnitario * Carrello.QuantitàCarrello).label('totcar')).join(Carrello).filter(Carrello.Mail_Cliente == current_user.Mail).filter(Semilavorati.Id == Carrello.Id_Semilavorato)

    if cart[0] == None and tot[0].totcar == None:
        Auxcarrello.totale = 0
        Auxcarrello.quantità = 0
    else:
        Auxcarrello.totale = round(float(tot[0].totcar), 2)
        Auxcarrello.quantità = cart[0]

    return redirect(url_for('ecommerce.shoping_cart'))

@ecommerce.route('/deleteWishlist/<id>')
@login_required
def deleteWishlist(id):
    delete_wishProd = WishList.query.filter(WishList.Mail_Cliente == current_user.Mail).filter(WishList.Id_Semilavorato == id)
    delete_wishProd.delete()
    db.session.commit()

    cart = session.query(func.sum(Carrello.QuantitàCarrello)).filter(Carrello.Mail_Cliente == current_user.Mail).first()
    tot = session.query(func.sum(Semilavorati.PrezzoUnitario * Carrello.QuantitàCarrello).label('totcar')).join(Carrello).filter(Carrello.Mail_Cliente == current_user.Mail).filter(Semilavorati.Id == Carrello.Id_Semilavorato)

    if cart[0] == None and tot[0].totcar == None:
        Auxcarrello.totale = 0
        Auxcarrello.quantità = 0
    else:
        Auxcarrello.totale = round(float(tot[0].totcar), 2)
        Auxcarrello.quantità = cart[0]

    return redirect(url_for('ecommerce.wishlist'))

@ecommerce.route('/addWishlist/<id>')
@login_required
def addWishlist(id):
    if WishList.query.filter(WishList.Mail_Cliente == current_user.Mail).filter(WishList.Id_Semilavorato == id).first() != None:
        flash('Questo prodotto è già nella tua WishList')
        return redirect(url_for('ecommerce.shop_details', id=id))
    else:
        new_wishProd = WishList(Mail_Cliente=current_user.Mail, Id_Semilavorato=id)
        db.session.add(new_wishProd)
        db.session.commit()
        return redirect(url_for('ecommerce.wishlist'))

