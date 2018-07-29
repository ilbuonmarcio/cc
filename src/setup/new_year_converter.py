import random

with open("spaggiari_output.csv", 'r') as input_file:
    input_array = []
    for line in input_file:
        input_array.append(line.split(';'))

        # NULL, 1, 2, 14, 13, NULL, 5, 3, 19, 10, 37, 39, NULL, NULL, 17, NULL, NULL, NULL

        
        # ID, COGNOME, NOME, MATRICOLA, CF, DESIDERATA, SESSO, DATANASCITA, CAP, NAZIONALITA, 170, 104,
        #       CLASSE PRECEDENTE, CLASSE SUCCESSIVA, INDIRIZZO, CODCAT, VOTO, IDGRUPPO

with open("spaggiari_output_elab.csv", 'w') as output_file:
    i = 1
    for line in input_array:
        record = [
            line[1].replace("'", "`"),
            line[2].replace("'", "`"),
            line[0],
            line[13],
            '',
            line[5],
            line[3] + ' 00:00',
            line[19],
            line[10],
            line[37] if line[37] != "NO" else "",
            line[39] if line[39] != "" else "",
            '',
            'NULL',
            random.randint(1, 5),
            'NULL',
            random.randint(6, 10)
        ]
        print(i, record, end="\n\n")
        if i == 1:
            pass
        else:
            for column in record:
                    output_file.write(str(column) + ",")



            output_file.write("\n")

        i+= 1

with open('spaggiari_output_elab.csv', 'r') as input_file:
    lines = input_file.readlines()

    with open('spaggiari_output_elab.csv', 'w') as output_file:
        for line in lines:
            line = line[:len(line)-2]
            print(line)
            output_file.write(line)
            output_file.write('\n')