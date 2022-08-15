from GenDB import *

Persone = [Persone(Mail='vioricadanci@gmail.com', Nome='Viorica', Cognome='Danci', Username='vioricadanci', Password='Viorica79', DataNascita='1979-07-12', Telefono='3283187029', Rating='0'),
           Persone(Mail='larissadanci@gmail.com', Nome='Larissa', Cognome='Danci', Username='larissadanci', Password='Larissa03', DataNascita='2003-03-01', Telefono='3205608445', Rating='0'),
           Persone(Mail='rominadanci@gmail.com', Nome='Romina', Cognome='Danci', Username='rominadanci', Password='Romina00', DataNascita='2000-01-20', Telefono='3290301407', Rating='0'),
           Persone(Mail='prova@gmail.com', Nome='Prova', Cognome='ProvaCognome', Username='prova', Password='Prova000', DataNascita='2003-03-01', Telefono='123456789', Rating='0')
           ]

Dipendenti = [Dipendenti(Mail='vioricadanci@gmail.com', DataAssunzione='11-07-2022'),
              Dipendenti(Mail='larissadanci@gmail.com', DataAssunzione='11-07-2022')]

Clienti = [Clienti(Mail='prova@gmail.com', DataRegistrazione='11-07-2022'),
           Clienti(Mail='rominadanci@gmail.com', DataRegistrazione='11-07-2022')]

DittaFornitrice = [DittaFornitrice(PartitaIVA='86334519757', Nome='StoccoSRL', Mail='stoccosrl@gmail.com', Telefono='0423406067', Via='Rossini 5', Città='Treviso', Stato='Italia'),
                   DittaFornitrice(PartitaIVA='88924578120', Nome='ColorantiSRL', Mail='colorantisrl@gmail.com', Telefono='0423807699', Via='San Marco 3', Città='Salzano', Stato='Italia'),
                   DittaFornitrice(PartitaIVA='89671233099', Nome='DolciariaSPA', Mail='dolciariaspa@gmail.com', Telefono='0423809766', Via='Cristoforo Colombo 15', Città='Treviso', Stato='Italia')]

Allergeni = [Allergeni(Nome='Cereali contenenti glutine'),
             Allergeni(Nome='Soia'),
             Allergeni(Nome='Frutta secca in guscio'),
             Allergeni(Nome='Arachidi'),
             Allergeni(Nome='Semi di sesamo'),
             Allergeni(Nome='Latte'),
             Allergeni(Nome='Uova'),
             Allergeni(Nome='Pesce'),
             Allergeni(Nome='Crostacei'),
             Allergeni(Nome='Sedano'),
             Allergeni(Nome='Senape'),
             Allergeni(Nome='Biossido di zolfo e solfiti'),
             Allergeni(Nome='Lupini'),
             Allergeni(Nome='Molluschi')]

Turni = [Turni(Nome='Mattiniero', OraInizioTurno='05:00:00', OraFineTurno='13:00:00', CompensoOrario='8.90'),
         Turni(Nome='Pomeridiano', OraInizioTurno='13:00:00', OraFineTurno='18:00:00', CompensoOrario='8.90'),
         Turni(Nome='Serale', OraInizioTurno='18:00:00', OraFineTurno='23:00:00', CompensoOrario='8.90'),
         Turni(Nome='Giornaliero', OraInizioTurno='05:00:00', OraFineTurno='17:00:00', CompensoOrario='8.90')]

Semilavorati = [Semilavorati(Nome='Brioche Crema', Quantità='20', PrezzoUnitario='1.10', IVA='10', Preparazione=None, Categoria='Brioche', Descrizione="", Incipit=""),
                Semilavorati(Nome='Brioche Cioccolato', Quantità='20', PrezzoUnitario='1.10', IVA='10', Preparazione=None, Categoria='Brioche', Descrizione="", Incipit=""),
                Semilavorati(Nome='Brioche Vuota', Quantità='20', PrezzoUnitario='1.10', IVA='10', Preparazione=None, Categoria='Brioche', Descrizione="", Incipit=""),
                Semilavorati(Nome='Brioche Marmellata', Quantità='20', PrezzoUnitario='1.10', IVA='10', Preparazione=None, Categoria='Brioche', Descrizione="", Incipit=""),
                Semilavorati(Nome='Brioche Frutti di bosco', Quantità='20', PrezzoUnitario='1.10', IVA='10', Preparazione=None, Categoria='Brioche', Descrizione="", Incipit="")]

Merce = [Merce(Nome='Farina', Quantità='10', PrezzoUnitario='5.00', IVA='10', MateriaPrima=True),
         Merce(Nome='Uova', Quantità='60', PrezzoUnitario='2.00', IVA='10', MateriaPrima=True),
         Merce(Nome='Burro', Quantità='20', PrezzoUnitario='4.00', IVA='10', MateriaPrima=True),
         Merce(Nome='Latte', Quantità='50', PrezzoUnitario='15.00', IVA='10', MateriaPrima=True),
         Merce(Nome='Gelatina', Quantità='10', PrezzoUnitario='25.00', IVA='10', MateriaPrima=True),
         Merce(Nome='Colorante Blu', Quantità='10', PrezzoUnitario='5.00', IVA='10', MateriaPrima=False),
         Merce(Nome='Colorante Rosa', Quantità='10', PrezzoUnitario='5.00', IVA='10', MateriaPrima=False),
         Merce(Nome='Colorante Rosso', Quantità='10', PrezzoUnitario='5.00', IVA='10', MateriaPrima=False),
         Merce(Nome='Colorante Nero', Quantità='10', PrezzoUnitario='5.00', IVA='10', MateriaPrima=False),
         Merce(Nome='Colorante Oro', Quantità='10', PrezzoUnitario='7.00', IVA='10', MateriaPrima=False),
         Merce(Nome='Colorante Argento', Quantità='10', PrezzoUnitario='7.00', IVA='10', MateriaPrima=False),
         Merce(Nome='Colorante Giallo', Quantità='10', PrezzoUnitario='5.00', IVA='10', MateriaPrima=False),
         Merce(Nome='Colorante Arancione', Quantità='10', PrezzoUnitario='5.00', IVA='10', MateriaPrima=False),
         Merce(Nome='Colorante Verde', Quantità='10', PrezzoUnitario='5.00', IVA='10', MateriaPrima=False)]

Articoli = [Articoli(Titolo='Ricette fresche per l estate', Categoria="", Contenuto='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus convallis ligula nec tempus posuere. Aliquam consequat ipsum eu viverra maximus. Nam lobortis, arcu a sollicitudin vulputate, enim odio efficitur mauris, et sollicitudin purus nisl at odio. Proin fringilla, urna posuere tristique cursus, lectus neque posuere diam, et posuere nibh tortor eget quam.', DataPubblicazione='21-07-2022'),
            Articoli(Titolo='Le cinque torte più richieste del mese', Categoria="", Contenuto='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus convallis ligula nec tempus posuere. Aliquam consequat ipsum eu viverra maximus. Nam lobortis, arcu a sollicitudin vulputate, enim odio efficitur mauris, et sollicitudin purus nisl at odio. Proin fringilla, urna posuere tristique cursus, lectus neque posuere diam, et posuere nibh tortor eget quam.', DataPubblicazione='21-07-2022'),
            Articoli(Titolo='NOVITA, Brioche variegate disponibili', Categoria="", Contenuto='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus convallis ligula nec tempus posuere. Aliquam consequat ipsum eu viverra maximus. Nam lobortis, arcu a sollicitudin vulputate, enim odio efficitur mauris, et sollicitudin purus nisl at odio. Proin fringilla, urna posuere tristique cursus, lectus neque posuere diam, et posuere nibh tortor eget quam.', DataPubblicazione='21-07-2022')]

Blog = [Blog(Mail_Dipendente='larissadanci@gmail.com', Id_Articolo=1),
        Blog(Mail_Dipendente='larissadanci@gmail.com', Id_Articolo=2),
        Blog(Mail_Dipendente='larissadanci@gmail.com', Id_Articolo=3)]

WishList = [WishList(Mail_Cliente='rominadanci@gmail.com', Id_Semilavorato=1),
            WishList(Mail_Cliente='rominadanci@gmail.com', Id_Semilavorato=3),
            WishList(Mail_Cliente='rominadanci@gmail.com', Id_Semilavorato=5),
            WishList(Mail_Cliente='prova@gmail.com', Id_Semilavorato=1),
            WishList(Mail_Cliente='prova@gmail.com', Id_Semilavorato=3),
            WishList(Mail_Cliente='prova@gmail.com', Id_Semilavorato=5)]

#Data = [Persone, Dipendenti, Clienti, DittaFornitrice, Allergeni, Turni, Semilavorati, Merce, Articoli]
Data = [ Blog, WishList]

for i in Data:
    session.add_all(i)

session.commit()

if __name__ == '__main__':
    app.run(debug=True)

