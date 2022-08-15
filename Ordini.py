from flask import Blueprint, render_template, request
from flask_login import current_user

ordini = Blueprint('ordini', __name__)

@ordini.route('/ordiniGestionale', methods=['GET', 'POST'])
def ordiniGestionale():
    list_ricevuti = []  # TODO QUERY
    list_emessi = []  # TODO QUERY
    if request.method == "POST":
        ricevuti = 0
        emessi = 0
        if request.form["nascosto"] == '1':
            ricevuti = request.form["ricevuti"]
        else:
            emessi = request.form["emessi"]
        #if(ricevuti == 1):
            # slider ricevuti avanti di 1
        #if(ricevuti == -1):
            # slider ricevuti indietro di 1
        # if(emessi == 1):
            # slider emessi avanti di 1
        # if(emessi == -1):
            # slider emessi indietro di 1
        return render_template("gestionale/ordini.html")
    else:
        #passare sempre i primi 10 elementi delle liste
        return render_template("gestionale/ordini.html")
