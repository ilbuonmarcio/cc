import sys
from pprint import pprint
import random


def show_usage():
    print(
        """
        Metodo di utilizzo:\n\n
        
        python converter.py {INPUT_FILE} {DESIDERATA_FILE} {OUTPUT_FILE} [UNIQUE_STUDENT_IDENTIFIER_COLUMN_INDEX]\n\n

        con parametro UNIQUE_STUDENT_IDENTIFIER_COLUMN_INDEX facoltativo, default --> colonna 1.

        Per informazioni: marciozgaming@gmail.com
        """
    )


def filter_input_file(input_file, unique_school_identifier_column=1):
    filtered_input_file = []

    headline = True
    for line in input_file:

        if headline: # Se è la prima riga contenente i nomi delle colonne, passa alla successiva
            headline = False
            continue

        record = [
            line[1].replace("'", "`"),
            line[2].replace("'", "`"),
            line[unique_school_identifier_column-1],
            line[13],
            "",
            line[5],
            line[3],
            line[19],
            line[10],
            line[37] if line[37] != "NO" else "",
            line[39] if line[39] != "" else "",
            'NULL',
            'NULL',
            random.randint(1, 5),
            'NULL',
            line[76] if line[76] in ["6", "7", "8", "9", "10"] else "7"
        ]

        filtered_input_file.append(record)

    return filtered_input_file


def insert_desiderata_into_input_file(input_file, desiderata_file):
    headline = True
    for line in desiderata_file:
        
        if headline: # Se è la prima riga contenente i nomi delle colonne, passa alla successiva
            headline = False
            continue
        
        line.append([]) # Array di cf per lo studente 1
        line.append([]) # Array di cf per lo studente 2

        for other_line in input_file:
            line_fullname = other_line[0] + ' ' + other_line[1]
            if line_fullname == line[0]:
                line[2].append(other_line[3]) # Aggiungo il codice fiscale dell'amico alla lista delle desiderate
            if line_fullname == line[1]:
                line[3].append(other_line[3]) # Aggiungo il codice fiscale dell'amico alla lista delle desiderate

        if len(line[2]) > 1 or len(line[3]) > 1: # Se ci sono ononimi
            print(f'Trovati degli ononimi: {line[0]} + {line[1]} --> Modificare desiderata manualmente')
        else: # Inserisco le desiderate
            line[2] = line[2][0] if line[2] != [] else ''
            line[3] = line[3][0] if line[3] != [] else ''
            for i in range(0, len(input_file)):
                line_fullname = input_file[i][0] + ' ' + input_file[i][1]
                if line_fullname == line[0]:
                    input_file[i][4] = line[3]
                elif line_fullname == line[1]:
                    input_file[i][4] = line[2]

    return input_file


if __name__ == "__main__":

    try:
        input_filename = sys.argv[1]
        desiderata_filename = sys.argv[2]
        output_filename = sys.argv[3]
        try:
            column_index = int(sys.argv[4])
        except:
            column_index = 1
    except:
        show_usage()
        exit(-1)

    input_file = []
    with open(input_filename, 'r', encoding='latin1') as f:
        input_file = [line.split(';') for line in f]

    desiderata_file = []
    with open(desiderata_filename, 'r', encoding='utf-8') as f:
        desiderata_file = [line.replace('"', '').replace("'", '`').split(',')[0:2] for line in f]


    input_file = filter_input_file(input_file, column_index)
    input_file = insert_desiderata_into_input_file(input_file, desiderata_file)
    with open(output_filename, 'w', encoding="utf-8") as f:
        for line in input_file:
            f.write(",".join(str(column) for column in line) + '\n')

    

    
    
