# Still Rings routine child class
# Inherits from Routine

from routine import Routine
import my_utilities as util
import skill

class RingsRoutine(Routine):
    # Object constructor
    def __init__(self, skills, numberOfSkills, hasEGIV, hasEGI, hasEGII, hasEGIII, isValid, countingElements, apparatus="Still Rings"):
        super().__init__(skills, numberOfSkills, hasEGIV, hasEGI, hasEGII, hasEGIII, isValid, countingElements, apparatus)
    
    # Overrides the default add_skill method
    # Function to add a skill to a routine
    # Parameters:
    # COP_conn - the sql connector to the MAG_COP.db database
    def add_skill(self, COP_conn):
        baseQuery = "SELECT skillName, skillValue, skillNumber FROM sr_eg_"
        cursor = COP_conn.cursor()
        # Prints options for selection and reads user input
        print("I. Kip and swing elements & swings through or to handstand.")
        print("II. Strength elements and hold elements (2 sec.).")
        print("III. Swing to Strength and hold elements (2 sec.).")
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
        if selection != "esc":
            # Creates an sql query to get the chosen skill
            assignQuery = "SELECT * FROM sr_eg_" + egString + " WHERE skillNumber = '" + selection + "';"
            #Executes the query and assigns the result to choice
            cursor.execute(assignQuery)
            choice = cursor.fetchone()        
            # Print the chosen skill and create a new skill object
            print(choice[0])
            newSkill = self.make_newSkill(choice, "new")
            print(choice)
            # Returns the chosen skill as an object
            return newSkill
        else:
            return "cancel"
        
    def make_newSkill(self, choice, task):
        if choice[3] == "I":
            newSkill = skill.RingsSkill(choice[0], choice[1], choice[2], choice[3], choice[4], choice[5], None)
        elif choice[3] == "II" or choice[3] == "III":
            newSkill = skill.RingsSkill(choice[0], choice[1], choice[2], choice[3], choice[4], None, choice[5])
        elif choice[3] == "IV":
            newSkill = skill.RingsSkill(choice[0], choice[1], choice[2], choice[3], choice[4], None, None)
        return newSkill
    
    def validate_routine(self):
        super().validate_routine()
        swingToHSExists = False
        for i in range(len(self.countingElements)):
            if self.countingElements[i].eg == "I" and self.countingElements[i].swingToHS == "1":
                swingToHSExists = True
        if not swingToHSExists:
            print("This routine does not have a swing to handstand element.")
            print("A rings routine needs to have one element within the couting 8 that is a swing to handstand.")
            self.isValid = False
    
    def special_repititions(self, skill):
        egIIstrengths = []
        egIIIstrengths = []
        if skill.eg == "II" or skill.eg == "III":
            for i in range(len(self.countingElements)):
                if self.countingElements[i].eg == "II":
                    egIIstrengths.append(self.countingElements[i].strengthShape)
                elif self.countingElements[i].eg == "III":
                    egIIIstrengths.append(self.countingElements[i].strengthShape)
            if skill.eg == "II":
                for i in range(len(egIIstrengths)):
                    if skill.strengthShape == egIIstrengths[i]:
                        return False
            elif skill.eg == "III":
                for i in range(len(egIIIstrengths)):
                    if skill.strengthShape == egIIIstrengths[i]:
                        return False
            else:
                return True
        else:
            return True

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
                       swingToHS,
                       strengthShape)'''.format(tableName))