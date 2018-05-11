with open("spaggiari_output.csv", 'r') as input_file:
    for line in input_file:
        [print(attribute) for attribute in line.split(';')]
        break
