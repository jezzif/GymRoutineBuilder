# Vault routine child class
# Inherits from Routine

from routine import Routine
import my_utilities as util
import skill

class VaultRoutine(Routine):
    # Object constructor
    def __init__(self, skills, numberOfSkills, hasEGIV, hasEGI, hasEGII, hasEGIII, isValid, countingElements, apparatus="Vault"):
        super().__init__(skills, numberOfSkills, hasEGIV, hasEGI, hasEGII, hasEGIII, isValid, countingElements, apparatus)
    
    def add_skill(self, COP_conn):
        baseQuery = "SELECT skillName, skillValue, skillNumber FROM vt_eg_"
        cursor = COP_conn.cursor()
        # Prints options for selection and reads user input
        print("I. Single salto vaults with complex twists.")
        print("II. Handspring salto vaults with or without simple twists, and all double salto fwd.")
        print("III. Handspring sideways and Tsukahara vaults with or without simple twists, and all double salto bwd.")
        print("IV. Round off entry and single salto vaults with complex twists.")
        print("V. Round off entry vaults with or without simple twists, and all double salto fwd. or bwd.")
        elementGroup = util.ReadIntegerRange("What element group do you want to see skills for? (1, 2, 3, 4, 5)", 1, 5)
        # Sets the last part of baseQuery to the correct element group
        if elementGroup == 1:
            egString = "i"
        elif elementGroup == 2:
            egString = "ii"
        elif elementGroup == 3:
            egString = "iii"
        elif elementGroup == 4:
            egString = "iv"
        elif elementGroup == 5:
            egString = "v"
        query = baseQuery + egString + ";"
        # Executes the sql query and prints the results
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows[1:]:
            print(row[0] + ", " + row[1] + ", " + row[2])
        # Calls choose_skill to read user input
        selection = self.choose_skill(rows)
        if selection != "esc":
            # Creates an sql query to get the chosen skill
            assignQuery = "SELECT * FROM vt_eg_" + egString + " WHERE skillNumber = '" + selection + "';"
            #Executes the query and assigns the result to choice
            cursor.execute(assignQuery)
            choice = cursor.fetchone()        
            # Print the chosen skill and create a new skill object
            print(choice[0])
            newSkill = self.make_newSkill(choice)
            print(choice)
            # Returns the chosen skill as an object
            return newSkill
        else:
            return "cancel"
        
    def make_newSkill(self, choice):
        newSkill = skill.Skill(choice[0], choice[1], choice[2], choice[3], choice[4])
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
                       skillNumber NOT NULL)'''.format(tableName))