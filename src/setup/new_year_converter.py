import random

with open("spaggiari_output.csv", 'r') as input_file:
    input_array = []
    for line in input_file:
        input_array.append(line.split(';'))

        # NULL, 1, 2, 14, 13, NULL, 5, 3, 19, 10, 37, 39, NULL, NULL, 17, NULL, NULL, NULL

        
        # ID, COGNOME, NOME, MATRICOLA, CF, DESIDERATA, SESSO, DATANASCITA, CAP, NAZIONALITA, 170, 104,
        #       CLASSE PRECEDENTE, CLASSE SUCCESSIVA, INDIRIZZO, CODCAT, VOTO, IDGRUPPO

with open("desiderata_elab.csv", 'r') as input_file2:
    array_2 = []
    for line in input_file2:
        array_2.append(line.split(','))

        # 0,               1,         2,        3
        
        # COGNOME NOME 1, CF 1, COGNOME NOME 2, CF 2

with open("spaggiari_output_elab.csv", 'w') as output_file:
    i = 1
    for line in input_array:
        desiderata = ""
        for line2 in array_2:
            if line2[1] == line[13]:
                desiderata = line2[3].replace("\n" , "")
            
            record = [
                line[1].replace("'", "`"),
                line[2].replace("'", "`"),
                line[0],
                line[13],
                desiderata,
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
                line[76] if line[76] in ["6", "7", "8", "9", "10"] else "6"
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
