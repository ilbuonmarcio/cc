import random

with open("db_app_desiderata_prime-export.csv", 'r') as input_file:
    input_array = []
    for line in input_file:
        input_array.append(line.split(','))

        # 0,             1,               2
        
        # COGNOME NOME 1, COGNOME NOME 2, MOTIVO

with open("spaggiari_output.csv", 'r') as file_2:
    array_2 = []
    for line in file_2:
        array_2.append(line.split(';'))

with open("desiderata_elab.csv", 'w') as output_file:
    i = 1
    
    for line in input_array:
        first_cf = ""
        second_cf = ""
        for line2 in array_2:
            if (line2[1].replace("'", "`") + " " + line2[2].replace("'", "`")) == line[0].replace("'", "`").replace('"', ''):
                first_cf = line2[13]
                break
            else:
                first_cf = ""
            
        for line3 in array_2:
            if (line3[1].replace("'", "`") + " " + line3[2].replace("'", "`")) == line[1].replace("'", "`").replace('"', ''):
                second_cf = line3[13]
                break
            else:
                second_cf = ""
          
        record = [
            line[0].replace("'", "`").replace('"', ''),
            first_cf,
            line[1].replace("'", "`").replace('"', ''),
            second_cf
                
        ]
        print(i, record, end="\n\n")
        if i == 1:
            pass
        else:
            for column in record:
                output_file.write(str(column) + ",")



            output_file.write("\n")

        i+= 1

with open('desiderata_elab.csv', 'r') as input_file:
    lines = input_file.readlines()

    with open('desiderata_elab.csv', 'w') as output_file:
        for line in lines:
            line = line[:len(line)-2]
            print(line)
            output_file.write(line)
            output_file.write('\n')
