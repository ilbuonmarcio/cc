from random import randint, choice
import string

nomi = ['Antonio', 'Lucia', 'Tiziano', 'Roberto', 'Fabio', 'Valentina', 'Alex', 'Giuseppe', 'Maria', 'Emanuele', 'Giacomo', 'Elia']
cognomi = ['Rossi', 'Verdi', 'Bianchi', 'Russo', 'Valentini', 'Roberti', 'Giannini', 'Scalco', 'Mirandola']
cf_list = []

num_campioni = 10

alunni = []

if __name__ == "__main__":
    for i in range(1, num_campioni + 1):
        c_id = i
        c_cognome = choice(cognomi)
        c_nome = choice(nomi)
        c_matricola = 20000 + i
        c_cf = "".join(
            [
                choice(string.hexdigits) for _ in range(0, 16)
            ]
        ).upper()
        cf_list.append(c_cf)

        c_desiderata = None
        c_sesso = choice(['m', 'f'])
        c_data_nascita = str(randint(1, 31)) + "/" + str(randint(1, 12)) + "/" + str(randint(2000, 2010))
        c_cap = randint(70000, 70075)
        c_nazionalita = choice(
            [
                "Italiana",
                "Arabica",
                "Albanese",
                "Francese",
                "Polacca",
                "Tedesca",
                "Spagnola",
                "Turca",
                "Australiana"
            ]
        )

        c_legge_107 = choice(['s', 'n'])
        c_legge_104 = choice(['s', 'n'])
        c_classe_precedente = None
        c_classe_successiva = None
        c_anno_scolastico = None
        c_scelta_indirizzo = choice([x for x in range(1, 6)])
        c_cod_cat = "".join(
            [
                choice(string.hexdigits) for _ in range(0, 4)
            ]
        ).upper()

        c_voto = randint(6, 10)
        c_id_gruppo = choice([1, 2, 3])

        alunni.append([
            c_id, #0
            c_cognome, #1
            c_nome, #2
            c_matricola, #3
            c_cf, #4
            c_desiderata, #5
            c_sesso, #6
            c_data_nascita, #7
            c_cap, #8
            c_nazionalita, #9
            c_legge_107, #10
            c_legge_104, #11
            c_classe_precedente, #12
            c_classe_successiva, #13
            c_scelta_indirizzo, #14
            c_cod_cat, #15
            c_voto, #16
            c_id_gruppo #17
        ])

    for alunno in alunni:
        while True:
            c = choice(cf_list)
            if c != alunno[4]:
                alunno[5] = c
                break

    for student in alunni:
        for other in alunni:
            if student[4] != other[4]:
                if student[4] == other[5] and student[5] == other[4]:
                    print("matched")

    with open('alunni_MYSQL.csv', 'w') as output_file:
        for alunno in alunni:
            output_file.write(alunno.__str__().replace(", ", ",").replace("'", '').replace('[', '').replace(']', '').replace('None', 'NULL') + "\n")

    with open('alunni_UPLOAD.csv', 'w') as output_file:
        for alunno in alunni:
            s = ""
            for i in range(0, len(alunno)):
                if i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16): # Valori interessanti per il modello di upload
                    if alunno[i] != None:
                        s += str(alunno[i])
                    s += ","
            s = s[:len(s)-1]
            print(s)
            output_file.write(s + "\n")
