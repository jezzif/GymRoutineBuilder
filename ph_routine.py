# Pommel Horse routine child class
# Inherits from Routine

from routine import Routine
import my_utilities as util
import skill

class PommelRoutine(Routine):
    # Object constructor
    def __init__(self, skills, numberOfSkills, hasEGIV, hasEGI, hasEGII, hasEGIII, isValid, countingElements, apparatus="Pommel Horse"):
        super().__init__(skills, numberOfSkills, hasEGIV, hasEGI, hasEGII, hasEGIII, isValid, countingElements, apparatus)
    # Overrides the default add_skill method
    # Function to add a skill to a routine
    # Parameters:
    # COP_conn - the sql connector to the MAG_COP.db database
    def add_skill(self, COP_conn):
        baseQuery = "SELECT skillName, skillValue, skillNumber FROM ph_eg_"
        cursor = COP_conn.cursor()
        # Prints options for selection and reads user input
        print("I. Single leg swings and scissors.")
        print("II. Circle and flairs, with and/or without spindles and handstands, Kehrswings, Russian wendeswings, flops and combined elements.")
        print("III. Travel type elements, including Tong Fei, Wu Guonian, Roth and Traveling Spindles")
        print("IV. Dismounts.")
        elementGroup = util.ReadIntegerRange("What element group do you want to see skills for? (1, 2, 3, 4)", 1, 4)
        # Sets the last part of baseQuery to the correct element group
        if elementGroup == 1:
            egString = "i"
        elif elementGroup == 2:
            egString = "ii"
        elif elementGroup == 3:
            egString = "iii"
        elif elementGroup == 4:
            egString = "iv"
        query = baseQuery + egString + ";"
        # Executes the sql query and prints the results
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows[1:]:
            print(row[0] + ", " + row[1] + ", " + row[2])
        # Calls choose_skill to read user input
        selection = self.choose_skill(rows)
        # Creates an sql query to get the chosen skill
        assignQuery = "SELECT * FROM ph_eg_" + egString + " WHERE skillNumber = '" + selection + "';"
        #Executes the query and assigns the result to choice
        cursor.execute(assignQuery)
        choice = cursor.fetchone()
        print(choice)
        # If the selection isn't cancelled:
        if selection != "esc":
            # Print the chosen skill and create a new skill object
            newSkill = self.make_newSkill(choice)
            # Returns the chosen skill as an object
            return newSkill
        else:
            return "cancel"
        
    def make_newSkill(self, choice):
        if choice[3] == "I" or choice[3] == "IV":
            newSkill = skill.PommelSkill(choice[0], choice[1], choice[2], choice[3], choice[4], None, None, None, None)
        elif choice[3] == "II":
            newSkill = skill.PommelSkill(choice[0], choice[1], choice[2], choice[3], choice[4], choice[5], None, None, None)
        elif choice[3] == "III":
            newSkill = skill.PommelSkill(choice[0], choice[1], choice[2], choice[3], choice[4], None, choice[5], choice[6], choice[7])
        return newSkill
    
    # Overrides the default make_table method
    # Procedure to make a new table in the Routines database
    # Parameters:
    # cursor - the cursor for the sql connector
    # tableName - the name of the table to be created
    def make_table(self, cursor, tableName):
        cursor.execute('''CREATE TABLE IF NOT EXISTS {}
                       (skillName NOT NULL,
                       skillDescr NOT NULL,
                       skillValue NOT NULL,
                       skillElemGrp NOT NULL,
                       skillNumber NOT NULL,
                       fullSpindle,
                       fullSpindleTravels,
                       fullCrossSupTravels,
                       fullRussianTravels)'''.format(tableName))