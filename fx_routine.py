# Floor exercise routine child class
# Inherits from Routine

from routine import Routine
import my_utilities as util
import skill

class FloorRoutine(Routine):
    # Object constructor
    def __init__(self, skills, numberOfSkills, hasEGIV, hasEGI, hasEGII, hasEGIII, isValid, countingElements, apparatus="Floor Exercise"):
        super().__init__(skills, numberOfSkills, hasEGIV, hasEGI, hasEGII, hasEGIII, isValid, countingElements, apparatus)

    # Overrides the default add_skill method
    # Function to add a skill to a routine
    # Parameters:
    # COP_conn - the sql connector to the MAG_COP.db database
    def add_skill(self, COP_conn):
        baseQuery = "SELECT skillName, skillValue, skillNumber FROM fx_eg_"
        cursor = COP_conn.cursor()
        # Prints options for selection and reads user input
        print("I. Non-acrobatic elements.")
        print("II. Acrobatic elements forward.")
        print("III. Acrobatic elements backward.")
        print("IV. Single salto forward and/or backward with 1 or more turns.")
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
            assignQuery = "SELECT * FROM fx_eg_" + egString + " WHERE skillNumber = '" + selection + "';"
            #Executes the query and assigns the result to choice
            cursor.execute(assignQuery)
            choice = cursor.fetchone()        
            # Print the chosen skill and create a new skill object
            print(len(choice))
            print(choice[0])
            print(choice[3])
            
            newSkill = self.make_newSkill(choice, "new")
            
            # Returns the chosen skill as an object
            return newSkill
        else:
            return "cancel"

    def make_newSkill(self, choice, task):
        if choice[3] == "I":
            newSkill = skill.FloorSkill(choice[0], choice[1], choice[2], choice[3], choice[4], False, choice[5], choice[6], choice[7], None)
        elif choice[3] == "II" or choice[3] == "III":
            if task == "new":
                newSkill = skill.FloorSkill(choice[0], choice[1], choice[2], choice[3], choice[4], False, None, None, None, choice[5])
            elif task == "view":
                newSkill = skill.FloorSkill(choice[0], choice[1], choice[2], choice[3], choice[4], False, None, None, None, choice[8])
        elif choice[3] == "IV":
            newSkill = skill.FloorSkill(choice[0], choice[1], choice[2], choice[3], choice[4], False, None, None, None, None)
        return newSkill
    
    def validate_routine(self):
        super().validate_routine()
        # print(self.skills[-1].name)
        # print(self.skills[-1].doubleSalto)
        if self.skills[-1].doubleSalto != "1":
            self.isValid = False
            print("This routine has no valid dismount.")
            print("A dismount in a floor exercise routine needs to be an multiple salto element.")
        oneLegBalance = False
        for i in range(len(self.skills)):
            if self.skills[i].oneLegBalance == "1":
                oneLegBalance = True
        if not oneLegBalance:
            print("This routine does not have a single leg balance element.")
            print("A floor routine needs to have a single leg balance element, but it does not have to be within the 8 counting elements.")
            self.isValid = False
    
    # Overrides the default special_repititions method
    # Function to check if the skill being possibly added to the counting elements exceeds the specific apparatuses
    # special repitition rules
    # Parameters:
    # skill - The skill being checked to be added to the counting elements
    def special_repititions(self, skill):
        strengthElementExists = False
        circleElementExists = False
        if skill.eg == "I":
            for i in range(len(self.countingElements)):
                if self.countingElements[i].strengthElement == "1":
                    strengthElementExists = True
                elif self.countingElements[i].circleElement == "1":
                    circleElementExists = True
            if skill.strengthElement == "1" and strengthElementExists == True:
                print("This routine has more than 1 strength element and only the higher value skill will be counted.")
                return False
            elif skill.circleElement == "1" and circleElementExists == True:
                print("This routine has more than 1 circle element and only the higher value skill will be counted.")
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
                       strengthElement, 
                       circleElement,
                       oneLegBalance,
                       doubleSalto)'''.format(tableName))