from flask import Blueprint, render_template, request
from flask_login import current_user

documenti = Blueprint('documenti', __name__)

@documenti.route('/documentiGestionale', methods=['GET', 'POST'])
def documentiGestionale():
    #TODO DA METTERE LE QUERY
    fatturaAcq = []
    fattureVen = []
    DTT = []
    scontrini = []

    if request.method == "POST":
        nascosto = request.form["nascosto"]
        if nascosto == '1':
            print(request.form["fattureAcq"])
            #if request.form["fatturaAcq"] == 1:
                # TODO SLIDER +1
            #else:
                # TODO SLIDE -1
        if nascosto == '2':
            print(request.form["fattureVen"])
            #if request.form["fatturaVen"] == 1:
                # TODO SLIDER +1
            #else:
                # TODO SLIDE -1
        if nascosto == '3':
            print(request.form["DDT"])
            #if request.form["DDT"] == 1:
                # TODO SLIDER +1
            #else:
                # TODO SLIDE -1
        if nascosto == '4':
            print(request.form["scontrini"])
            #if request.form["scontrini"] == 1:
                # TODO SLIDER +1
            #else:
                # TODO SLIDE -1

        return render_template("gestionale/documenti.html")
    else:
        return render_template("gestionale/documenti.html")

@documenti.route('/bilancioGestionale')
def bilancioGestionale():
    return render_template("gestionale/bilancio.html")

@documenti.route('/bilancioCosti')
def bilancioCosti():
    return render_template("gestionale/")

@documenti.route('/bilancioRicavi')
def bilancioRicavi():
    return render_template("gestionale/")

@documenti.route('/ricevuti')
def ricevuti():
    return render_template("gestionale/")

@documenti.route('/emessi')
def emessi():
    return render_template("gestionale/")

@documenti.route('/cassa')
def cassa():
    return render_template("gestionale/")
