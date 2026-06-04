import my_utilities as util
import skill
import csv
import tableMaker
import sqlite3

class Routine:

    def __init__(self, skills, numberOfSkills, hasEGIV, hasEGI, hasEGII, hasEGIII, isValid, countingElements, apparatus):
        self.skills = skills
        self.numberOfSkills = numberOfSkills
        self.hasEGIV = hasEGIV
        self.hasEGI = hasEGI
        self.hasEGII = hasEGII
        self.hasEGIII = hasEGIII
        self.isValid = isValid
        self.countingElements = countingElements
        self.apparatus = apparatus

    # Procedure that prints the skills of a routine in a way that is easily read
    def print_skills(self):
        for i in range(self.numberOfSkills):
            # print(str(self.skills[i].order) + ": " + self.skills[i].name + ", "
            #         + self.skills[i].description + " Value: " + self.skills[i].value 
            #         + " (" + self.skills[i].eg + "." + self.skills[i].number + ")")
            print(str(i + 1) + ": " + self.skills[i].name + ", "
                    + self.skills[i].description + " Value: " + self.skills[i].value 
                    + " (" + self.skills[i].eg + "." + self.skills[i].number + ")")
            
    def special_repititions(self, skill):
        return True
    
    # Procedure that checks if the routine meets all of the FIG requirements.
    def validate_routine(self):
        self.isValid = True
        # Determine the counting elements of the routine
        sortedSkills = sorted(self.skills, key=lambda skill: skill.value, reverse=True)
        iTaken = 0
        iiTaken = 0
        iiiTaken = 0
        ivTaken = 0
        i = 0
        
        # Adds the highest value skill from each element group to satisfy the element group bonus
        while i < len(sortedSkills):
            #print(f"Skill: {sortedSkills[i].name}, EG: {sortedSkills[i].eg}")
            if sortedSkills[i].eg == "I" and iTaken < 1:
                self.countingElements.append(sortedSkills.pop(i))
                iTaken += 1
            elif sortedSkills[i].eg == "II" and iiTaken < 1:
                self.countingElements.append(sortedSkills.pop(i))
                iiTaken += 1
            elif sortedSkills[i].eg == "III" and iiiTaken < 1:
                self.countingElements.append(sortedSkills.pop(i))
                iiiTaken  += 1
            elif sortedSkills[i].eg == "IV" and ivTaken < 1:
                self.countingElements.append(sortedSkills.pop(i))
                ivTaken += 1
            else:
                i += 1
        # print("Counting elements initial:")
        # for i in range(len(self.countingElements)):
        #     print(self.countingElements[i].name)
        # print()
        if self.apparatus == "Still Rings":
            swingToHSExists = False
            for i in range(len(self.countingElements)):
                if self.countingElements[i].eg == "I" and self.countingElements[i].swingToHS == "1":
                    swingToHSExists = True
            i = 0
            print(len(sortedSkills))
            while i < len(sortedSkills) and not swingToHSExists:
                print(f"Iteration: {i}")
                print(sortedSkills[i].name)
                if sortedSkills[i].eg == "I" and sortedSkills[i].swingToHS == "1":
                    self.countingElements.append(sortedSkills.pop(i))
                    swingToHSExists = True
                else:
                    i += 1

        # Sets the amount of times for the next loop to iterate
        # to avoid index out of range if there are less than 8 skills in the routine
        if len(self.skills) < 8:
            topRange = len(self.skills)
        else:
            topRange = 8

        # Changes the max number of skills allowed in element group 4 
        if self.apparatus == "Floor Exercise":
            ivMax = 4
        else:
            ivMax = 1

        # Adds the remaining highest value skills until 8 skills are reached.
        # Checks if the skill conforms to the special repitition rules.
        for i in range(topRange - len(self.countingElements)):
            print(f"I: {iTaken}, II: {iiTaken}, III: {iiiTaken}, IV: {ivTaken}")
            append = False
            if sortedSkills[i].eg == "I" and iTaken < 4:
                append = self.special_repititions(sortedSkills[i])
                if append:
                    iTaken += 1
            elif sortedSkills[i].eg == "II" and iiTaken < 4:
                append = self.special_repititions(sortedSkills[i])
                if append:
                    iiTaken += 1
            elif sortedSkills[i].eg == "III" and iiiTaken < 4:
                append = self.special_repititions(sortedSkills[i])
                if append:
                    iiiTaken += 1     
            elif sortedSkills[i].eg == "IV" and ivTaken < ivMax:
                append = self.special_repititions(sortedSkills[i])
                if append:
                    ivTaken += 1
            for j in range(len(self.countingElements)):
                if sortedSkills[i].eg == self.countingElements[j].eg and sortedSkills[i].number == self.countingElements[j].number:
                    append = False
                    print("This routine has duplicate skills, a skill can only count toward the D-score once.")
                    break
            if append:
                self.countingElements.append(sortedSkills[i])
                # print(f"Appending {sortedSkills[i].name}")
        print("COUNTING ELEMENTS")
        for i in range(len(self.countingElements)):
            print(self.countingElements[i].name)

        # Checks how many skills the routine has
        if self.numberOfSkills < 6:
            print(f"Routine does not have enough elements. 6 elements are required, this routine only has {str(self.numberOfSkills)} elements.")
        elif self.numberOfSkills > 8:
            print("Routine has more than 8 skills.")
            print("More than 8 skills can be included but, only 8 skills including the dismount can contribute to the D-score of a routine.")
        else:
            print("Routine has enough skills.")
        if self.hasEGI > 4:
            print("This routine has more than 4 skills from element group 1, only the 4 highest will be counted.")
        if self.hasEGII > 4:
            print("This routine has more than 4 skills from element group 2, only the 4 highest will be counted.")
        if self.hasEGIII > 4:
            print("This routine has more than 4 skills from element group 3, only the 4 highest will be counted.")
        if self.apparatus != "Floor Exercise" and self.hasEGIV > 1:
            self.isValid = False
            print("This routine has more than 1 dismount and isn't a valid routine")
        elif self.hasEGIV > 4:
            print("This routine has more than 4 skills from element group 4, only the 4 highest will be counted.")
            
        print()

    # Function that calculates the D-score of any given routine
    def calculate_D_score(self):
        print("Calculating D score.")
        difficultyTotal = 0
        total = 0
        for i in range(len(self.countingElements)):
            difficultyTotal += float(self.countingElements[i].value)
             #Sums the difficulty value of all elements
        print(f"Values of all skills: {difficultyTotal}")
        total = round(difficultyTotal, 1)
        #Calculates connection bonuses
        if self.apparatus == "floor exercise" or self.apparatus == "horizontal bar":
            print("Connection bonus calculations.")
        #Awards element group requirement value
        added = False
        if self.hasEGI > 0:
            total += 0.5
            print(f"Adding 0.5 for EG I. Current total: {total}")
        if self.hasEGII > 0:
            for i in range(len(self.countingElements) - 1):
                if self.countingElements[i].eg == "II" and float(self.countingElements[i].value) > 0.3:
                    total += 0.5
                    added = True
                    print(f"Adding 0.5 for EG II.  Current total: {total}")
                    break
            if not added:
                total += 0.3
                print(f"Adding 0.3 for EG II.  Current total: {total}")
        added = False
        if self.hasEGIII > 0:
            for i in range(len(self.countingElements) - 1):
                if self.countingElements[i].eg == "III" and float(self.countingElements[i].value) > 0.3:
                    total += 0.5
                    added = True
                    print(f"Adding 0.5 for EG III.  Current total: {total}")
                    break
            if not added:
                total += 0.3
                print(f"Adding 0.3 for EG III.  Current total: {total}")
        added = False
        if self.hasEGIV > 0:
            print(f"Apparatus: {self.apparatus}")
            if self.apparatus != "Floor Exercise":
                total += float(self.skills[-1].value)
                print(f"Adding value of the dimsount. Current total: {total}")
            else:
                for i in range(len(self.countingElements) - 1):
                    if self.countingElements[i].eg == "IV" and float(self.countingElements[i].value) > 0.3:
                        total += 0.5
                        added = True
                        print(f"Adding 0.5 for EG IV.  Current total: {total}")
                        break
                if not added:
                    total += 0.3
                    print(f"Adding 0.3 for EG IV.  Current total: {total}")
        total = round(total, 1)
        return total

    # Function that selects a skill
    # Could add to remove_skill() would need to re-add operation parrameter
    # Parameters:
    # skills - A 2D array of every skill in the specific element group
    def choose_skill(self, skills):
        quit = False
        valid = False
        # Loops until a a skill has been chosen or the operation is cancelled
        while not quit:
            # User inputs what skill they want to add
            selection = str(input("What skill do you want to add? Choose skills by number in last column. Type 'esc' to cancel. "))
            if selection == "esc":
                break
            # Checks to see if input is in the skills list
            for row in skills[1:]:
                if selection in row[2]:
                    valid = True
                    quit = True
                    break
            # Gives feedback if the skill isn't entered
            if valid == False:
                print("That skill does not exist")
        # Returns the number of the chosen skill
        return selection
    
    # Procedure to remove a skill from a routine
    # Could add choose_skill()
    def remove_skill(self):
        print("Which skill do you want to remove? (Choose based on number in first column) ")
        #Prints all skills
        self.print_skills()
        choice = util.ReadIntegerRange("", 1, self.numberOfSkills)
        #Removes the skill
        if self.skills[choice - 1].eg == "I":
            self.hasEGI -= 1
        elif self.skills[choice - 1].eg == "II":
            self.hasEGII -= 1
        elif self.skills[choice - 1].eg == "III":
            self.hasEGIII -= 1
        elif self.skills[choice - 1].eg == "IV":
            self.hasEGIV -= 1
        self.skills.pop(choice - 1)
        self.numberOfSkills -= 1
        #SHOULDN'T NEED ORDER
        #Resolves index
        #Doesn't work if first item is removed.
        # for i in range(self.numberOfSkills):
        #     index = i + 1
        #     self.skills[i].order = index

    #Procedure to swap the position of two skills
    def swap_skills(self):
        #Asks for user input
        print("What skills do you want to swap (Choose based on number in first column)")
        self.print_skills()
        choice1 = util.ReadIntegerRange("First skill to swap: ", 1, self.numberOfSkills) - 1
        choice2 = util.ReadIntegerRange("Second skill to swap:", 1, self.numberOfSkills) - 1
        #Swaps the skills and then fixes the changed order number
        self.skills[choice1], self.skills[choice2] = self.skills[choice2], self.skills[choice1]
        #self.skills[choice1].order, self.skills[choice2].order = self.skills[choice2].order, self.skills[choice1].order

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
        

    # Procedure to add, swap or remove skills from a routine
    # Parameters:
    # tableName - the name of the table in the database for the current routine
    # new_routine_check - is the routine being created or edited, True if routine is being created.
    # Routines_conn - the sql connector to the Routines.db database
    # COP_conn - the sql connector to the MAG_COP.db database
    def build_routine(self, tableName, new_routine_check, Routines_conn, COP_conn):    
        quit = False
        match self.apparatus:
            case "Floor Exercise":
                current_conn = Routines_conn.FXR_conn
            case "Pommel Horse":
                current_conn = Routines_conn.PHR_conn
            case "Still Rings":
                current_conn = Routines_conn.SRR_conn
            case "Vault":
                current_conn = Routines_conn.VTR_conn
            case "Parallel Bars":
                current_conn = Routines_conn.PBR_conn
            case "Horizontal Bar":
                current_conn = Routines_conn.HBR_conn
        cursor = current_conn.cursor()
        # Asks user to name their routine if it is new
        if new_routine_check == True:
            tableName = input("Name of routine? ")
            # Makes a new table in the Routines.db database
            self.make_table(cursor, tableName)
        # Loops until the user quits
        while (not quit):
            # User inputs their choice for what they want to do
            action = util.ReadIntegerRange("Add a skill (1), Remove a skill (2), Swap order of skills (3), Finish (4), Cancel (5)", 1, 5)
            match action:
                case 1: # Add a skill
                    newSkill = self.add_skill(COP_conn)
                    # Adds the newSkill object to the Routine object's list of skills
                    #print("build_routine check " + newSkill.doubleSalto)
                    if newSkill != "cancel":
                        self.skills.append(newSkill)
                        self.numberOfSkills += 1
                case 2: # Remove a skill
                    self.remove_skill()
                case 3:
                    self.swap_skills()
                case 4: # Finish and save
                    # Reset the table
                    deleteStatement = "DELETE FROM {}".format(tableName)
                    cursor.execute(deleteStatement)

                    # sql query for inserting skills
                    insertStatement = "INSERT INTO {} (skillName, skillDescr, skillValue, skillElemGrp, skillNumber".format(tableName)
                    
                    if self.apparatus == "Floor Exercise":
                        # sql query for inserting skills
                        insertStatement += ", strengthElement, circleElement, oneLegBalance, doubleSalto) VALUES(?,?,?,?,?,?,?,?,?)"
                        # Creates an array for the sql query to execute from
                        contents = []
                        for i in range(len(self.skills)):
                            contents.append([self.skills[i].name, self.skills[i].description, self.skills[i].value, self.skills[i].eg, self.skills[i].number, self.skills[i].strengthElement, self.skills[i].circleElement, self.skills[i].oneLegBalance, self.skills[i].doubleSalto])
                    elif self.apparatus == "Pommel Horse":
                        # sql query for inserting skills
                        insertStatement += ", fullSpindle, fullSpindleTravels, fullCrossSupTravels, fullRussianTravels) VALUES(?,?,?,?,?,?,?,?,?)"
                        # Creates an array for the sql query to execute from
                        contents = []
                        for i in range(len(self.skills)):
                            contents.append([self.skills[i].name, self.skills[i].description, self.skills[i].value, self.skills[i].eg, self.skills[i].number, self.skills[i].fullSpindle, self.skills[i].fullSpindleTravels, self.skills[i].fullCrossSupTravels, self.skills[i].fullRussianTravels])
                    elif self.apparatus == "Still Rings":
                        # sql query for inserting skills
                        insertStatement += ", swingToHS, strengthShape) VALUES(?,?,?,?,?,?,?)"
                        # Creates an array for the sql query to execute from
                        contents = []
                        for i in range(len(self.skills)):
                            contents.append([self.skills[i].name, self.skills[i].description, self.skills[i].value, self.skills[i].eg, self.skills[i].number, self.skills[i].swingToHS, self.skills[i].strengthShape])
                    elif self.apparatus == "Vault":
                        # sql query for inserting skills
                        insertStatement += ") VALUES(?,?,?,?,?)"
                        # Creates an array for the sql query to execute from
                        contents = []
                        for i in range(len(self.skills)):
                            contents.append([self.skills[i].name, self.skills[i].description, self.skills[i].value, self.skills[i].eg, self.skills[i].number])
                    elif self.apparatus == "Parallel Bars":
                        # sql query for inserting skills
                        insertStatement += ", fwdUprise, giantSwing, felgeSwing) VALUES(?,?,?,?,?,?,?,?)"
                        # Creates an array for the sql query to execute from
                        contents = []
                        for i in range(len(self.skills)):
                            contents.append([self.skills[i].name, self.skills[i].description, self.skills[i].value, self.skills[i].eg, self.skills[i].number, self.skills[i].fwdUprise, self.skills[i].giantSwing, self.skills[i].felgeSwing])
                    elif self.apparatus == "Horizontal Bar":
                        # sql query for inserting skills
                        insertStatement += ", adlerType) VALUES(?,?,?,?,?,?)"
                        # Creates an array for the sql query to execute from
                        contents = []
                        for i in range(len(self.skills)):
                            contents.append([self.skills[i].name, self.skills[i].description, self.skills[i].value, self.skills[i].eg, self.skills[i].number, self.skills[i].adlerType])

                    # Inserts the skills into the table
                    cursor.executemany(insertStatement, contents)
                    # Saves the changes made
                    current_conn.commit()
                    print("Saved.")
                    quit = True
                case 5: # Cancels the changes
                    quit = True