__author__ = "Leonardo Bonomi, Mattia Carra"
__version__ = "0.1"
__date__ = "2018-04-10"
"""
Programma python per la composizione classi progetto MarconiCC
"""

# -- IMPORT
import mysql.connector
import pprint
    
# -- CLASSI
class Alunno:
    def __init__(self, id, cognome, nome, matricola, CF, desiderata, sesso, data_nascita, cap, nazionalita,
                 legge_107, legge_104, classe_precedente, classe_successiva, scelta_indirizzo, cod_cat, voto, id_gruppo):
        self.id = id
        self.cognome = cognome
        self.nome = nome
        self.matricola = matricola
        self.CF = CF
        self.desiderata = desiderata
        self.sesso = sesso
        self.data_nascita = data_nascita
        self.cap = cap
        self.nazionalita = nazionalita
        self.legge_107 = legge_107
        self.legge_104 = legge_104
        self.classe_precedente = classe_precedente
        self.classe_successiva = classe_successiva
        self.scelta_indirizzo = scelta_indirizzo
        self.cod_cat = cod_cat
        self.voto = voto
        self.id_gruppo = id_gruppo

# -- FUNZIONI
def list_alunni():
    connection = mysql.connector.connect(user='root', password='', host='localhost', database='composizioneclassi')
    cursor = connection.cursor()
    query = ("SELECT * FROM alunni")        
    cursor.execute(query)
    array_alunni = []
    
    for (id, cognome, nome, matricola, CF, desiderata, sesso, data_nascita, cap, nazionalita, legge_107, legge_104, classe_precedente,
         classe_successiva, scelta_indirizzo, cod_cat, voto, id_gruppo) in cursor:
         dictionary_alunni = {}
         dictionary_alunni['id'] = id
         dictionary_alunni['cognome'] = cognome
         dictionary_alunni['nome'] = nome
         dictionary_alunni['matricola'] = matricola
         dictionary_alunni['CF'] = CF
         dictionary_alunni['desiderata'] = desiderata
         dictionary_alunni['sesso'] = sesso
         dictionary_alunni['data_nascita'] = data_nascita
         dictionary_alunni['cap'] = cap
         dictionary_alunni['nazionalita'] = nazionalita
         dictionary_alunni['legge_107'] = legge_107
         dictionary_alunni['legge_104'] = legge_104
         dictionary_alunni['classe_precedente'] = classe_precedente
         dictionary_alunni['classe_successiva'] = classe_successiva
         dictionary_alunni['scelta_indirizzo'] = scelta_indirizzo
         dictionary_alunni['cod_cat'] = cod_cat
         dictionary_alunni['voto'] = voto
         dictionary_alunni['id_gruppo'] = id_gruppo
         array_alunni.append(dictionary_alunni)
         pprint.pprint((array_alunni))

    cursor.close()
    connection.close()

# -- ELABORAZIONE
if __name__ == "__main__":
    list_alunni()



    
    
    
    
