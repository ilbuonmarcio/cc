import random

lines_to_write = []
with open('last_year.csv', 'r') as input_file:

    for line in input_file:
        line = line.replace("'", "").split(';')
        output_record = ""
        for i in range(0, 11):
            if i == 2 and line[i] == '':
                line[2] = str(random.randint(50000, 99999))
            output_record += line[i] + ","

        output_record += ",NULL,"
        output_record += f"{random.randint(1, 5)},NULL,"
        output_record += line[15] if line[15] in range(1, 11) else "6"

        output_record += "\n"

        lines_to_write.append(output_record)

with open('last_year_UPLOAD.csv', 'w') as output_file:
    for line in lines_to_write:
        output_file.write(line)
