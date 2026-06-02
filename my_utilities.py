import csv
    
# Function that reads user input and validates that it is an integer between to set numbers
# Parameters:
# prompt - the message to be displayed to the user
# lower - the value that the entered integer must be larger than
# upper - the value that the entered integer must be smaller than
def ReadIntegerRange(prompt, lower, upper):
    valid = False
    while not valid:
        while True:
            try:
                number = int(input(prompt))
                break
            except ValueError:
                print("Please enter an integer.")
        if number < lower or number > upper:
            print("Please input a number in between " + str(lower) + " and " + str(upper))
        else:
            valid = True
    return number
   
# Then reads the csv file into a list
# Parameters:
# fileName - the name and path of the file to be read
def read_csv(fileName):
    #Reading csv file
    file = open(fileName)
    csvReader = csv.reader(file)
    header = []
    header = next(csvReader)
    rows = []
    for row in csvReader:
        rows.append(row)
    if len(header) > 7:
        apparatus = header[7]
    else:
        apparatus = False
    file.close()
    return header, rows, apparatus