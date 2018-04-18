__author__ = "Leonardo Bonomi, Mattia Carra"
__version__ = "1.0"
__date__ = "2018-04-10"
"""
Python program for the composition of classes of Project MarconiCC
"""

# -- IMPORT
import mysql.connector
import tkinter
from tkinter import messagebox

# -- VARIABILI
# hide main window
root = tkinter.Tk()
root.withdraw()
    
# -- CLASSI
class Alunno:
    def __init__(self, id, cognome, nome, matricola, CF, desiderata, sesso, data_nascita, cap, nazionalita, legge_170, legge_104, classe_precedente, classe_successiva, scelta_indirizzo, cod_cat, voto, id_gruppo):
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
        self.legge_170 = legge_170
        self.legge_104 = legge_104
        self.classe_precedente = classe_precedente
        self.classe_successiva = classe_successiva
        self.scelta_indirizzo = scelta_indirizzo
        self.cod_cat = cod_cat
        self.voto = voto
        self.id_gruppo = id_gruppo

class Config:
    def __init__(self, id, nome, min_alunni, max_alunni, numero_femmine, numero_maschi, max_per_cap, max_per_naz, max_naz, num_170):
        self.id = id
        self.nome = nome
        self.min_alunni = min_alunni
        self.max_alunni = max_alunni
        self.numero_femmine = numero_femmine
        self.numero_maschi = numero_maschi
        self.data_nascita = data_nascita
        self.max_per_cap = max_per_cap
        self.max_per_naz = max_per_naz
        self.max_naz = max_naz
        self.num_170 = num_170
        

# -- FUNZIONI
def list_alunni():
    try:
        connection = mysql.connector.connect(user='root', password='', host='localhost', database='composizioneclassi')
        cursor = connection.cursor()
        query = ("SELECT * FROM alunni WHERE id_gruppo = 3")        
        cursor.execute(query)
        dictionary_alunni = dict()

        for (id, cognome, nome, matricola, CF, desiderata, sesso, data_nascita, cap, nazionalita, legge_170, legge_104, classe_precedente, classe_successiva, scelta_indirizzo, cod_cat, voto, id_gruppo) in cursor:
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
            dictionary_alunni['legge_170'] = legge_170
            dictionary_alunni['legge_104'] = legge_104
            dictionary_alunni['classe_precedente'] = classe_precedente
            dictionary_alunni['classe_successiva'] = classe_successiva
            dictionary_alunni['scelta_indirizzo'] = scelta_indirizzo
            dictionary_alunni['cod_cat'] = cod_cat
            dictionary_alunni['voto'] = voto
            dictionary_alunni['id_gruppo'] = id_gruppo
            if (len(dictionary_alunni.keys())) != 0:
                print(dictionary_alunni)
            else:
                # message box display
                messagebox.showerror("Error", "Empty result set")     
                
        cursor.close()
        connection.close()
    except:
        messagebox.showerror("Error", "Impossible to connect to the database")


def list_config():
    try:
        connection = mysql.connector.connect(user='root', password='', host='localhost', database='composizioneclassi')
        cursor = connection.cursor()
        query = ("SELECT * FROM configurazioni WHERE id = 1")        
        cursor.execute(query)
        dictionary_configurazioni = dict()

        for (id, nome, min_alunni, max_alunni, numero_femmine, numero_maschi, max_per_cap, max_per_naz, max_naz, num_170) in cursor:
            dictionary_alunni['id'] = id
            dictionary_alunni['nome'] = nome
            dictionary_alunni['min_alunni'] = min_alunni
            dictionary_alunni['max_alunni'] = max_alunni
            dictionary_alunni['numero_femmine'] = numero_femmine
            dictionary_alunni['numero_maschi'] = numero_maschi
            dictionary_alunni['max_per_cap'] = max_per_cap
            dictionary_alunni['max_per_naz'] = max_per_naz
            dictionary_alunni['max_naz'] = max_naz
            dictionary_alunni['num_170'] = num_170
            print(dictionary_configurazioni)
                
        cursor.close()
        connection.close()
    except:
        messagebox.showerror("Error", "Impossible to connect to the database")        

# -- ELABORAZIONE
if __name__ == "__main__":
    #get the result from $hello variable found in myPHPScript.php   //prendere il risultato di una variabile da un file php
    list_alunni()
    #list_config()




 

 




    
    
    
    
