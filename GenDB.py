from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

#TODO 1. Sistema questione immagini, sistema Q.tà delle ricette e per quante persone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgresql@localhost:5432/pasticceria"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

engine = create_engine("postgresql://postgres:postgresql@localhost:5432/pasticceria")

Session = sessionmaker(bind=engine)

session = Session()

class Immagini(db.Model):
    __tablename__ = 'immagini'

    Id = db.Column(db.Integer(), primary_key=True)
    img = db.Column(db.String())

    Persona = relationship("Persone", back_populates = "Immagine")

    Articolo = relationship("ImmaginiArticoli", back_populates='Immagine', cascade="all, delete-orphan")
    Semilavorato = relationship("ImmaginiSemilavorati", back_populates='Immagine', cascade="all, delete-orphan")
    Merce = relationship("ImmaginiMerce", back_populates='Immagine', cascade="all, delete-orphan")

    def __init__(self, img):
        self.img = img

    def __repr__(self):
        return f"<Immagini {self.Id}>"

class Persone(db.Model, UserMixin):
    __tablename__ = 'persone'

    Mail = db.Column(db.String(60), primary_key=True)
    Nome = db.Column(db.String(60), nullable=False)
    Cognome = db.Column(db.String(60), nullable=False)
    Username = db.Column(db.String(60), nullable=False, unique=True)
    Password = db.Column(db.String(500), nullable=False)
    DataNascita = db.Column(db.Date(), nullable=False)
    Telefono = db.Column(db.String(15), nullable=False)
    Rating = db.Column(db.Integer)

    Img = db.Column(ForeignKey('immagini.Id', ondelete='CASCADE'))
    Immagine = relationship("Immagini", back_populates = 'Persona')

    Dipendente = relationship("Dipendenti", back_populates = "Persona")
    Cliente = relationship("Clienti", back_populates = "Persona")

    def __init__(self, Mail, Nome, Cognome, Username, Password, DataNascita, Telefono, Rating):
        self.Mail = Mail
        self.Nome = Nome
        self.Cognome = Cognome
        self.Username = Username
        self.Password = bcrypt.generate_password_hash(Password).decode('utf-8')
        self.DataNascita = DataNascita
        self.Telefono = Telefono
        self.Rating = Rating

    def get_id(self):
        return (self.Mail)

    def __repr__(self):
        return f"<Persona {self.Mail}>"

class Dipendenti(db.Model):
    __tablename__ = 'dipendenti'

    Mail = db.Column(ForeignKey('persone.Mail', ondelete='CASCADE'), primary_key = True)
    DataAssunzione = db.Column(db.Date(), nullable=False)

    Persona = relationship("Persone", back_populates = 'Dipendente')

    Stipendio = relationship("Stipendi", back_populates = "Dipendente") #da fare relazione

    Articolo = relationship("Blog", back_populates='Dipendente',  cascade="all, delete-orphan")
    Turno = relationship("PersonaleTurni", back_populates='Dipendente',  cascade="all, delete-orphan")

    def __init__(self, Mail, DataAssunzione):
        self.Mail = Mail
        self.DataAssunzione = DataAssunzione

    def __repr__(self):
        return f"<Dipendente {self.Mail}>"

class Clienti(db.Model):
    __tablename__ = 'clienti'

    Mail = db.Column(ForeignKey('persone.Mail', ondelete='CASCADE'), primary_key = True)
    DataRegistrazione = db.Column(db.Date(), nullable=False)
    IndirizzoSpedizione = db.Column(db.String(100)) #da ricontrollare

    Persona = relationship("Persone", back_populates="Cliente")
    Messaggio = relationship("Messaggi", back_populates="Cliente")
    Commento = relationship("Commenti", back_populates="Cliente")

    Semilavorato_WishList = relationship("WishList", back_populates='Cliente_WishList',  cascade="all, delete-orphan")
    Semilavorato_Carrello = relationship("Carrello", back_populates='Cliente_Carrello',  cascade="all, delete-orphan")

    def __init__(self, Mail, DataRegistrazione):
        self.Mail = Mail
        self.DataRegistrazione = DataRegistrazione

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f"<Cliente {self.Mail}>"

class DittaFornitrice(db.Model):
    __tablename__ = 'dittaFornitrice'

    PartitaIVA = db.Column(db.String(11), primary_key=True)
    Nome = db.Column(db.String(60), nullable=False)
    Mail = db.Column(db.String(50), nullable=False)
    Telefono = db.Column(db.String(15), nullable=False)
    Via = db.Column(db.String(50))
    Città = db.Column(db.String(50))
    Stato = db.Column(db.String(50))

    DDT = relationship("DDT", back_populates = "Fornitore")
    FatturaAcquisto = relationship("FattureAcquisto", back_populates = "Fornitore")

    def __init__(self, PartitaIVA, Nome, Mail, Telefono, Via, Città, Stato):
        self.PartitaIVA = PartitaIVA
        self.Nome = Nome
        self.Mail = Mail
        self.Telefono = Telefono
        self.Via = Via
        self.Città = Città
        self.Stato = Stato

    def __repr__(self):
        return f"<Fornitore {self.PartitaIVA}>"

class DDT(db.Model):
    __tablename__ = 'ddt'

    Id = db.Column(db.Integer(), primary_key=True)
    Id_Fornitore = db.Column(db.String(11), ForeignKey("dittaFornitrice.PartitaIVA", ondelete='CASCADE'))
    NumDocumento = db.Column(db.Integer(), nullable=False)
    DataEmissione = db.Column(db.Date(), nullable=False)
    Note = db.Column(db.String(500))    #q.tà dei beni trasportati per voce, aspetto esteriore, descrizione
    Importo = db.Column(db.Float(), nullable=False)
    Peso = db.Column(db.Float())
    Colli = db.Column(db.Integer())

    Fornitore = relationship("DittaFornitrice", back_populates="DDT")

    def __init__(self, Mail_Fornitore, DataEmissione, Note, Importo, Peso, Colli):
        self.Mail_Fornitore = Mail_Fornitore
        self.DataEmissione = DataEmissione
        self.Note = Note
        self.Importo = Importo
        self.Colli = Colli
        self.Peso = Peso

    def __repr__(self):
        return f"<DDT {self.Id}>"

class Stipendi(db.Model):
    __tablename__ = 'stipendi'

    Id = db.Column(db.Integer(), primary_key=True)
    Mail_Dipendenti = db.Column(db.String(60), ForeignKey('dipendenti.Mail', ondelete='CASCADE')) #da fare, VEDI SE VA MESSO
    DataEmissione = db.Column(db.Date(), nullable=False)
    ImportoNetto = db.Column(db.Float(), nullable=False)

    Dipendente = relationship("Dipendenti", back_populates="Stipendio")

    def __init__(self, Mail_Dipedendente, DataEmissione, ImportoNetto):
        self.Mail_Dipendenti = Mail_Dipedendente
        self.DataEmissione = DataEmissione
        self.ImportoNetto = ImportoNetto

    def __repr__(self):
        return f"<Stipendi {self.Id}>"

class Articoli(db.Model):
    __tablename__ = 'articoli'

    Id = db.Column(db.Integer(), primary_key=True)
    Titolo = db.Column(db.String(60))
    Contenuto = db.Column(db.String(500))
    DataPubblicazione = db.Column(db.Date())
    Categoria = db.Column(db.String())

    Dipendente = relationship("Blog", back_populates='Articolo', cascade="all, delete-orphan")
    Immagine = relationship("ImmaginiArticoli", back_populates='Articolo', cascade="all, delete-orphan")

    def __init__(self, Titolo, Contenuto, DataPubblicazione, Categoria):
        self.Titolo = Titolo
        self.Contenuto = Contenuto
        self.DataPubblicazione = DataPubblicazione
        self.Categoria = Categoria

    def __repr__(self):
        return f"<Articolo {self.Id}>"

class Turni(db.Model):
    __tablename__ = 'turni'

    Id = db.Column(db.Integer(), primary_key=True)
    Nome = db.Column(db.String(60), nullable=False)
    OraInizioTurno = db.Column(db.Time(), nullable=False)
    OraFineTurno = db.Column(db.Time(), nullable=False)
    CompensoOrario = db.Column(db.Float(), nullable=False)

    Dipendente = relationship("PersonaleTurni", back_populates='Turno', cascade="all, delete-orphan")

    def __init__(self, Nome, OraInizioTurno, OraFineTurno, CompensoOrario):
        self.Nome = Nome
        self.OraInizioTurno = OraInizioTurno
        self.OraFineTurno = OraFineTurno
        self.CompensoOrario = CompensoOrario

    def __repr__(self):
        return f"<Turni {self.Id}>"

class Semilavorati(db.Model):
    __tablename__ = 'semilavorati'

    Id = db.Column(db.Integer(), primary_key=True)
    Nome = db.Column(db.String(60), nullable=False, unique=True)
    Quantità = db.Column(db.Integer(), nullable=False)
    PrezzoUnitario = db.Column(db.Float(), nullable=False)
    IVA = db.Column(db.Float())
    Preparazione = db.Column(db.String(1000))
    Categoria = db.Column(db.String(60))
    Descrizione = db.Column(db.String(500))
    Preferito = db.Column(db.Boolean())
    Incipit = db.Column(db.String(100))

    Scontrino = relationship("ScontriniSemilavorati", back_populates='Semilavorato',  cascade="all, delete-orphan")
    Merce = relationship("Ricette", back_populates='Semilavorato', cascade="all, delete-orphan")
    Cliente_WishList = relationship("WishList", back_populates='Semilavorato_WishList',  cascade="all, delete-orphan")
    Cliente_Carrello = relationship("Carrello", back_populates='Semilavorato_Carrello',  cascade="all, delete-orphan")
    Produzione = relationship("Produzione", back_populates='Semilavorato',  cascade="all, delete-orphan")
    FatturaVendita = relationship("ContenutoVenditaSemilavorati", back_populates='Semilavorato', cascade="all, delete-orphan")
    Immagine = relationship("ImmaginiSemilavorati", back_populates='Semilavorato', cascade="all, delete-orphan")

    def __init__(self, Nome, Quantità, PrezzoUnitario, IVA, Preparazione, Categoria, Descrizione, Incipit):
        self.Nome = Nome
        self.Quantità = Quantità
        self.PrezzoUnitario = PrezzoUnitario
        self.IVA = IVA
        self.Preparazione = Preparazione
        self.Categoria = Categoria
        self.Descrizione = Descrizione
        self.Incipit = Incipit

    def __repr__(self):
        return f"<Semilavorati {self.Id}>"

class Scontrini(db.Model):
    __tablename__ = 'scontrini'

    Id = db.Column(db.Integer(), primary_key=True)
    Data = db.Column(db.Date(), nullable=False)

    Semilavorato = relationship("ScontriniSemilavorati", back_populates='Scontrino', cascade="all, delete-orphan")
    Merce = relationship("ScontriniMerce", back_populates='Scontrino',  cascade="all, delete-orphan")

    def __init__(self, Data):
        self.Data = Data

    def __repr__(self):
        return f"<scontrini {self.Id}>"

class Allergeni(db.Model):
    __tablename__ = 'allergeni'

    Id = db.Column(db.Integer(), primary_key=True)
    Nome = db.Column(db.String(60), nullable=False, unique=True)

    Merce = relationship("Merce", back_populates = "Allergene")

    def __init__(self, Nome):
        self.Nome = Nome

    def __repr__(self):
        return f"<allergeni {self.Id}>"

class Merce(db.Model):
    __tablename__ = 'merce'

    Id = db.Column(db.Integer(), primary_key=True)
    Nome = db.Column(db.String(60), nullable=False)
    Quantità = db.Column(db.Integer())
    PrezzoUnitario = db.Column(db.Float())
    IVA = db.Column(db.Float())
    MateriaPrima = db.Column(db.Boolean())  #ATTENZIONE, solo se True può far parte di una ricetta
    Id_Allergene = db.Column(ForeignKey('allergeni.Id', ondelete='CASCADE')) #vedi se è da mettere nel costruttore

    Allergene = relationship("Allergeni", back_populates = "Merce")

    Semilavorato = relationship("Ricette", back_populates='Merce', cascade="all, delete-orphan")
    Scontrino = relationship("ScontriniMerce", back_populates='Merce', cascade="all, delete-orphan")
    FatturaAcquisto = relationship("ContenutoAcquisto", back_populates='Merce',  cascade="all, delete-orphan")
    FatturaVendita = relationship("ContenutoVenditaMerce", back_populates='Merce',  cascade="all, delete-orphan")
    Immagine = relationship("ImmaginiMerce", back_populates='Merce', cascade="all, delete-orphan")

    def __init__(self, Nome, Quantità, PrezzoUnitario, IVA, MateriaPrima):
        self.Nome = Nome
        self.Quantità = Quantità
        self.PrezzoUnitario = PrezzoUnitario
        self.IVA = IVA
        self.MateriaPrima = MateriaPrima

    def __repr__(self):
        return f"<Merce {self.Id}>"

class ProduzioneGiornaliera(db.Model):
    __tablename__ = 'produzioneGiornaliera'

    Data = db.Column(db.Date(), primary_key=True)
    Note = db.Column(db.String(500))

    Semilavorato = relationship("Produzione", back_populates='Produzione', cascade="all, delete-orphan")

    def __init__(self, Data, Note):
        self.Data = Data
        self.Note = Note

    def __repr__(self):
        return f"<produzioneGiornaliera {self.Data}>"

class FattureAcquisto(db.Model):
    __tablename__ = 'fattureAcquisto'

    Id = db.Column(db.Integer(), primary_key=True)
    Id_Fornitore = db.Column(db.String(11), ForeignKey('dittaFornitrice.PartitaIVA', ondelete='CASCADE'))
    NumDocumento = db.Column(db.Integer(), nullable=False)
    Data = db.Column(db.Date(), nullable=False)

    Fornitore = relationship("DittaFornitrice", back_populates="FatturaAcquisto")

    NotaVariazioneRicevute = relationship("NoteVariazioneRicevute", back_populates = "FatturaAcquisto")

    Merce = relationship("ContenutoAcquisto", back_populates='FatturaAcquisto',  cascade="all, delete-orphan")

    def __init__(self, Mail_Fornitore, NumDocumento, Data):
        self.Mail_Fornitore = Mail_Fornitore
        self.NumDocumento = NumDocumento
        self.Data = Data

    def __repr__(self):
        return f"<FattureAcquisto {self.Id}>"

class FattureVendita(db.Model):
    __tablename__ = 'fattureVendita'

    Id = db.Column(db.Integer(), primary_key=True)
    Mail_Cliente = db.Column(db.String(60), ForeignKey('clienti.Mail', ondelete='CASCADE'))
    NumDocumento = db.Column(db.Integer(), nullable=False)
    Data = db.Column(db.Date(), nullable=False)

    NotaVariazioneEmesse = relationship("NoteVariazioneEmesse", back_populates = "FatturaVendita")

    Merce = relationship("ContenutoVenditaMerce", back_populates='FatturaVendita', cascade="all, delete-orphan")
    Semilavorato = relationship("ContenutoVenditaSemilavorati", back_populates='FatturaVendita',  cascade="all, delete-orphan")

    def __init__(self, Mail_Fornitore, NumDocumento, Data):
        self.Mail_Fornitore = Mail_Fornitore
        self.NumDocumento = NumDocumento
        self.Data = Data

    def __repr__(self):
        return f"<FattureVendita {self.Id}>"

class NoteVariazioneRicevute(db.Model):
    __tablename__ = 'noteVariazioneRicevute'

    Id = db.Column(db.Integer(), primary_key=True)
    Id_fatturaAcquisto = db.Column(db.Integer(), ForeignKey('fattureAcquisto.Id', ondelete='CASCADE'))
    NumDocumento = db.Column(db.Integer(), nullable=False)
    Data = db.Column(db.Date(), nullable=False)
    Note = db.Column(db.String(500))
    Variazione = db.Column(db.Float())

    FatturaAcquisto = relationship("FattureAcquisto", back_populates = "NotaVariazioneRicevute")

    def __init__(self, Id_fatturaAcquisto, NumDocumento, Data, Note, Variazione):
        self.Id_fatturaAcquisto = Id_fatturaAcquisto
        self.NumDocumento = NumDocumento
        self.Data = Data
        self.Note = Note
        self.Variazione = Variazione

    def __repr__(self):
        return f"<NotediVariazioneRicevute {self.Id}>"

class NoteVariazioneEmesse(db.Model):
    __tablename__ = 'noteVariazioneEmesse'

    Id = db.Column(db.Integer(), primary_key=True)
    Id_fatturaVendita = db.Column(db.Integer(), ForeignKey('fattureVendita.Id', ondelete='CASCADE'))
    NumDocumento = db.Column(db.Integer(), nullable=False)
    Data = db.Column(db.Date(), nullable=False)
    Note = db.Column(db.String(500))
    Variazione = db.Column(db.Float())

    FatturaVendita = relationship("FattureVendita", back_populates = "NotaVariazioneEmesse")

    def __init__(self, Id_fatturaVendita, NumDocumento, Data, Note, Variazione):
        self.Id_fatturaVendita = Id_fatturaVendita
        self.NumDocumento = NumDocumento
        self.Data = Data
        self.Note = Note
        self.Variazione = Variazione

    def __repr__(self):
        return f"<NotediVariazioneEmesse {self.Id}>"

class Messaggi(db.Model):
    __tablename__ = 'messaggi'

    Id = db.Column(db.Integer(), primary_key=True)
    Testo = db.Column(db.String(800))
    Oggetto = db.Column(db.String(100))
    Mail_Cliente = db.Column(db.String(), ForeignKey('clienti.Mail', ondelete='CASCADE'))

    Cliente = relationship("Clienti", back_populates="Messaggio")

    def __init__(self, Testo, Oggetto, Mail_Cliente):
        self.Testo = Testo
        self.Oggetto = Oggetto
        self.Mail_Cliente = Mail_Cliente

    def __repr__(self):
        return f"<messaggio {self.Data}>"

class Commenti(db.Model):
    __tablename__ = 'commenti'

    Id = db.Column(db.Integer(), primary_key=True)
    Testo = db.Column(db.String(500))
    Utente = db.Column(db.String(), ForeignKey('clienti.Mail', ondelete='CASCADE'))
    Risposta = db.Column(db.Integer(), ForeignKey('commenti.Id', ondelete='CASCADE'))

    Cliente = relationship("Clienti", back_populates="Commento")
    Commento = relationship("Commenti")

    def __init__(self, Testo, Utente, Risposta):
        self.Testo = Testo
        self.Utente = Utente
        self.Risposta = Risposta

    def __repr__(self):
        return f"<commento {self.Data}>"


#assciazione diendeti articoli
class Blog(db.Model):
    __tablename__ = 'blog'

    Mail_Dipendente = db.Column(ForeignKey('dipendenti.Mail', ondelete='CASCADE'), primary_key = True)
    Id_Articolo = db.Column(ForeignKey('articoli.Id', ondelete='CASCADE'), primary_key = True)

    Dipendente = relationship('Dipendenti', back_populates='Articolo')
    Articolo = relationship('Articoli', back_populates='Dipendente')

#assciazione personale turni
class PersonaleTurni(db.Model):
    __tablename__ = 'personaleTurni'

    Mail_Dipendente = db.Column(ForeignKey('dipendenti.Mail', ondelete='CASCADE'), primary_key=True)
    Id_Turno = db.Column(ForeignKey('turni.Id', ondelete='CASCADE'), primary_key=True)
    Data = db.Column(db.Date())
    OraInizio = db.Column(db.Time())
    OraFine = db.Column(db.Time())

    Dipendente = relationship('Dipendenti', back_populates='Turno')
    Turno = relationship('Turni', back_populates='Dipendente')

# associazione tra materie prime e semilavorati
class Ricette(db.Model):
    __tablename__ = 'ricette'

    Id_Semilavorato = db.Column(ForeignKey('semilavorati.Id', ondelete='CASCADE'), primary_key=True)
    Id_MateriaPrima = db.Column(ForeignKey('merce.Id', ondelete='CASCADE'), primary_key=True)   #in quanto specificato che solo le merci che sono materie prime possono comporre ricette
    Quantita = db.Column(db.Integer())
    Tempo = db.Column(db.Time())

    Semilavorato = relationship('Semilavorati', back_populates='Merce')
    Merce = relationship('Merce', back_populates='Semilavorato')

#assciazione clienti semilavorati
class WishList(db.Model):
    __tablename__ = 'wishList'

    Mail_Cliente = db.Column(ForeignKey('clienti.Mail', ondelete='CASCADE'), primary_key=True)
    Id_Semilavorato = db.Column(ForeignKey('semilavorati.Id', ondelete='CASCADE'), primary_key=True)

    Cliente_WishList = relationship('Clienti', back_populates='Semilavorato_WishList')
    Semilavorato_WishList = relationship('Semilavorati', back_populates='Cliente_WishList')

#assciazione clienti semilavorati
class Carrello(db.Model):
    __tablename__ = 'carrello'

    Mail_Cliente = db.Column(ForeignKey('clienti.Mail', ondelete='CASCADE'), primary_key=True)
    Id_Semilavorato = db.Column(ForeignKey('semilavorati.Id', ondelete='CASCADE'), primary_key=True)
    QuantitàCarrello = db.Column(db.Integer())

    Cliente_Carrello = relationship('Clienti', back_populates='Semilavorato_Carrello')
    Semilavorato_Carrello = relationship('Semilavorati', back_populates='Cliente_Carrello')

#assciazione produzioneGiornaliera semilavorati
class Produzione(db.Model):
    __tablename__ = 'produzione'

    Data_Produzione = db.Column(ForeignKey('produzioneGiornaliera.Data', ondelete='CASCADE'), primary_key=True)
    Id_Semilavorato = db.Column(ForeignKey('semilavorati.Id', ondelete='CASCADE'), primary_key=True)
    Quantità = db.Column(db.Integer())

    Produzione = relationship('ProduzioneGiornaliera', back_populates='Semilavorato')
    Semilavorato = relationship('Semilavorati', back_populates='Produzione')

#assciazione scontrini semilavorati
class ScontriniSemilavorati(db.Model):
    __tablename__ = 'scontriniSemilavorati'

    Id_Scontrino = db.Column(ForeignKey('scontrini.Id', ondelete='CASCADE'), primary_key=True)
    Id_Semilavorato = db.Column(ForeignKey('semilavorati.Id', ondelete='CASCADE'), primary_key=True)
    Quantità = db.Column(db.Integer())

    Scontrino = relationship('Scontrini', back_populates='Semilavorato')
    Semilavorato = relationship('Semilavorati', back_populates='Scontrino')

#assciazione scontrini merce
class ScontriniMerce(db.Model):
    __tablename__ = 'scontriniMerce'

    Id_Scontrino = db.Column(ForeignKey('scontrini.Id', ondelete='CASCADE'), primary_key=True)
    Id_Merce = db.Column(ForeignKey('merce.Id', ondelete='CASCADE'), primary_key=True)
    Quantità = db.Column(db.Integer())

    Scontrino = relationship('Scontrini', back_populates='Merce')
    Merce = relationship('Merce', back_populates='Scontrino')

#assciazione fatture acquisto merce
class ContenutoAcquisto(db.Model):
    __tablename__ = 'contenutoAcquisto'

    Id_FatturaAcquisto = db.Column(ForeignKey('fattureAcquisto.Id', ondelete='CASCADE'), primary_key=True)
    Id_Merce = db.Column(ForeignKey('merce.Id', ondelete='CASCADE'), primary_key=True)
    Quantità = db.Column(db.Integer())

    FatturaAcquisto = relationship('FattureAcquisto', back_populates='Merce')
    Merce = relationship('Merce', back_populates='FatturaAcquisto')

#assciazione fatture vendita merce
class ContenutoVenditaMerce(db.Model):
    __tablename__ = 'contenutoVenditaMerce'

    Id_FatturaVendità = db.Column(ForeignKey('fattureVendita.Id', ondelete='CASCADE'), primary_key=True)
    Id_Merce = db.Column(ForeignKey('merce.Id', ondelete='CASCADE'), primary_key=True)
    Quantità = db.Column(db.Integer())

    FatturaVendita = relationship('FattureVendita', back_populates='Merce')
    Merce = relationship('Merce', back_populates='FatturaVendita')

# assciazione fatture vendita semilavorati
class ContenutoVenditaSemilavorati(db.Model):
    __tablename__ = 'contenutoVenditaSemilavorati'

    Id_FatturaVendità = db.Column(ForeignKey('fattureVendita.Id', ondelete='CASCADE'), primary_key=True)
    Id_Semilavorato = db.Column(ForeignKey('semilavorati.Id', ondelete='CASCADE'), primary_key=True)
    Quantità = db.Column(db.Integer())

    FatturaVendita = relationship('FattureVendita', back_populates='Semilavorato')
    Semilavorato = relationship('Semilavorati', back_populates='FatturaVendita')

# assciazione immagini articoli
class ImmaginiArticoli(db.Model):
    __tablename__ = 'immaginiArticoli'

    Id_Articolo = db.Column(ForeignKey('articoli.Id', ondelete='CASCADE'), primary_key=True)
    Id_Img = db.Column(ForeignKey('immagini.Id', ondelete='CASCADE'), primary_key=True)

    Articolo = relationship('Articoli', back_populates = 'Immagine')
    Immagine = relationship('Immagini', back_populates = 'Articolo')

# assciazione immagini semilarorati
class ImmaginiSemilavorati(db.Model):
    __tablename__ = 'immaginiSemilavorati'

    Id_Semilavorato = db.Column(ForeignKey('semilavorati.Id', ondelete='CASCADE'), primary_key=True)
    Id_Img = db.Column(ForeignKey('immagini.Id', ondelete='CASCADE'), primary_key=True)

    Semilavorato = relationship('Semilavorati', back_populates='Immagine')
    Immagine = relationship('Immagini', back_populates='Semilavorato')

# assciazione immagini merce
class ImmaginiMerce(db.Model):
    __tablename__ = 'immaginiMerce'

    Id_Merce = db.Column(ForeignKey('merce.Id', ondelete='CASCADE'), primary_key=True)
    Id_Img = db.Column(ForeignKey('immagini.Id', ondelete='CASCADE'), primary_key=True)

    Merce = relationship('Merce', back_populates='Immagine')
    Immagine = relationship('Immagini', back_populates='Merce')

