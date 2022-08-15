# Tirocinio
## Progetto di tirocinio: Gestionale pasticceria
Nella nostra proposta di tirocinio e tesi vorremmo presentare il progetto per la realizzazione di un sistema dedicato ad una specifica pasticceria.
Questo strumento deve garantire l’integrale controllo degli aspetti contabili ed organizzativi dell’attività, inoltre vogliamo proporre una comoda vetrina per il sito della pasticceria ove possa presentare i diversi servizi e prodotti che potrebbe offrire.
Tutto ciò presentato sotto forma di una WebApp.
Un'altra componente che abbiamo pensato per il sistema è un’applicazione dedicata al personale dipendente dell’attività, che verrà approfondita nei prossimi paragrafi.

### WebApp
Questa componente del sistema a sua volta è composta da:
Gestionale, privato dedicato al titolare
Sito, pubblico dedicato alle interazioni con i clienti
Dal sito sarà possibile accedere al gestionale attraverso un login presente nella sezione area riservata.
##### Descrizione Gestionale
Qui troviamo la possibilità di gestire diversi aspetti contabili e organizzativi dell’attività, elencandoli sono:
- Fornitori
  - Ingredienti, giacenze di magazzino
  - Ordini, acquisto materie prime
- Clienti
  - Anagrafe clienti, gestione dei clienti profilizzati 
  - Storico ordini
- Ricettario, elenco ricette per lancio di produzione
- Documenti, gestione, visione e creazione dei documenti necessari
  - DDT
  - Fatture
  - Note di credito
  - Storico documenti
- Costi, anagrafica dei costi 
  - Gestione del personale
  - Gestione infrastrutturali
  - Gestione ingredienti
  - Costi fiscali
- Ricavi, anagrafica ricavi
  - Gestione vendite (e-commerce)
  - Gestione vendite (in loco), registrate manualmente
- Lancio di produzione, organizzazione della produzione 
    - Produzione giornaliera, scheduling produzione
    - Extra, attività non ordinarie

##### Descrizione del sito 
Qui troviamo le diverse componenti che vanno a formare la vetrina che la pasticceria può sfruttare per l’autopromozione dei propri servizi e prodotti offerti. Elenchiamo le voci che abbiamo pensato per il sito, sono:
- Team, presentazione del personale di lavoro
- La pasticceria, presentazione generale dell’attività, dei servizi e prodotti offerti (HomePage)
- Contatti
- Servizi e prodotti
  - Shop, e-commerce dedicato al Take Away e al Delivery
    - Prodotti, listino dei prodotti offerti
  - Prenotazione tavolo
  - Catering, possibilità di ingaggiare l’attività per servizio di catering ad eventi speciali
- Blog, aggiornamenti costanti relativi all’attività

![uml_webapp](https://github.com/Ghita00/Tirocinio/blob/master/Image_ReadMe/UML_WebApp.jpg "uml_webapp")

### Applicazione
##### Descrizione applicazione
Abbiamo pensato a questa componente aggiuntiva del sistema per garantire una più comoda gestione del personale e dei costi associati ad esso. 
Quest’applicazione è interamente dedicata ai dipendenti per:
- Consultazione orari e turni di lavoro
- Sistema Qr Code per la gestione delle presenze 

![uml_app](https://github.com/Ghita00/Tirocinio/blob/master/Image_ReadMe/UML_App.jpg "uml_app")

#### Architettura e tecnologie del sistema
L'architettura finale del sistema presenta un DataBase centrale con il quale andranno ad interagire (in lettura e in scrittura) sia la WebApp (sito + gestionale) che l’applicazione.
Le tecnologie da noi pensate sono:
- HTML e CSS per la presentazione
- JavaScript per le gestioni delle API
- Python con la libreria Flask per la gestione BackEnd 
- Postgresql per la gestione del DataBase
- Python con la libreria SQLAlchemy per le interrogazioni al DataBase
- Kotlin per l’applicazione

![Architettura](https://github.com/Ghita00/Tirocinio/blob/master/Image_ReadMe/architettura.png "Architettura")

<!--
  TODO
  - Aggiungere DB
  - ...
-->



