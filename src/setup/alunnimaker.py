from random import randint, choice
import string

nomi = ['Antonio', 'Lucia', 'Tiziano', 'Roberto', 'Fabio', 'Valentina', 'Alex', 'Giuseppe', 'Maria', 'Emanuele', 'Giacomo', 'Elia']
cognomi = ['Rossi', 'Verdi', 'Bianchi', 'Russo', 'Valentini', 'Roberti', 'Giannini', 'Scalco', 'Mirandola']
cf_list = []

num_campioni = 500

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
        c_anno_scolastico = "2018/2019"
        c_scelta_indirizzo = choice([x for x in range(1, 6)])
        c_cod_cat = "".join(
            [
                choice(string.hexdigits) for _ in range(0, 4)
            ]
        ).upper()

        c_voto = randint(6, 10)
        c_id_gruppo = choice([1, 2, 3])

        alunni.append([
            c_id,
            c_cognome,
            c_nome,
            c_matricola,
            c_cf,
            c_desiderata,
            c_sesso,
            c_data_nascita,
            c_cap,
            c_nazionalita,
            c_legge_107,
            c_legge_104,
            c_classe_precedente,
            c_classe_successiva,
            c_anno_scolastico,
            c_scelta_indirizzo,
            c_cod_cat,
            c_voto,
            c_id_gruppo
        ])

    for alunno in alunni:
        while True:
            c = choice(cf_list)
            if c != alunno[4]:
                alunno[5] = c
                break

    with open('alunni.csv', 'w') as output_file:
        for alunno in alunni:
            output_file.write(alunno.__str__().replace(", ", ",").replace("'", '').replace('[', '').replace(']', '').replace('None', 'NULL') + "\n")
