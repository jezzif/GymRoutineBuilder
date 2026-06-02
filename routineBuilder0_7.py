#16/06/2024

import routine
from fx_routine import FloorRoutine
from ph_routine import PommelRoutine
from sr_routine import RingsRoutine
from vt_routine import VaultRoutine
from pb_routine import PbarsRoutine
from hb_routine import HbarRoutine
import skill
import os
import my_utilities as util
import tableMaker
import connectors
import sqlite3

class Program:
    def main(self):
        while True:
            #Create or load Code of Points database on local machine.
            COP_conn = sqlite3.connect("Databases\\MAG_COP.db")
            #Routines_conn = sqlite3.connect("Databases\\Routines.db")
            Routines_conn = connectors.Connectors()
            #tableMaker.test(COP_conn)
            #tableMaker.delete(Routines_conn)
            #tableMaker.populate(COP_conn)
            

            '''cursor = conn.execute("SELECT skillName, skillValue from vt_eg_v")
            for row in cursor:
                print("NAME = ", row[0])
                print("VALUE = ", row[1])
            listOfTables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            print(listOfTables)'''


            #What does the user want to do
            choice = util.ReadIntegerRange("What do you want to do? Build a new routine (1), View existing routines (2), Quit (3)", 1, 3)
            if choice == 1:
                #Tells function that this routine is being created and not edited
                new_routine_check = True
                #Routine for what apparatus?
                print("What apparatus do you want to build a routine for?")
                apparatusChoice = util.ReadIntegerRange("Floor Exercise (1), Pommel Horse (2), Still Rings (3), Vault (4), Parallel Bars (5), Horizontal Bar (6)", 1, 6)
                match apparatusChoice:
                    case 1:
                        currentRoutine = FloorRoutine([],0,0,0,0,0,False,[])
                        apparatus = "FX"
                    case 2:
                        currentRoutine = PommelRoutine([],0,0,0,0,0,False,[])
                        apparatus = "PH"
                    case 3:
                        currentRoutine = RingsRoutine([],0,0,0,0,0,False,[])
                        apparatus = "SR"
                    case 4:
                        currentRoutine = VaultRoutine([],0,0,0,0,0,False,[])
                        apparatus = "VT"
                    case 5:
                        currentRoutine = PbarsRoutine([],0,0,0,0,0,False,[])
                        apparatus = "PB"
                    case 6:
                        currentRoutine = HbarRoutine([],0,0,0,0,0,False,[])
                        apparatus = "HB"
                currentRoutine.build_routine("", new_routine_check, Routines_conn, COP_conn)
            elif choice == 2:
                self.view_routines(self, False, 0, Routines_conn, COP_conn)
            elif choice == 3:
                break
            else:
                continue

    def view_routines(self, skip, routineToOpen, Routines_conn, COP_conn):
        #Prints all files in the "Routines" folder
        routineList = []
        apparatuses = []
        connList = [Routines_conn.FXR_conn,
                    Routines_conn.PHR_conn,
                    Routines_conn.SRR_conn,
                    Routines_conn.VTR_conn,
                    Routines_conn.PBR_conn,
                    Routines_conn.HBR_conn]
        for i in range(6):
            cursor = connList[i].cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            rows = cursor.fetchall()
            for row in rows:
                routineList.append(row[0])
                apparatuses.append(connList[i])
        if (not routineList):
            print("There are no existing routines.")
        else:
            if not skip:
                #Opens the selected routine
                print("Which routine would you like to view?")
                print(routineList)
                routineToOpen = input() #The routine
            #Checks if routine exists
            if routineToOpen in routineList:
                routineIndex = routineList.index(routineToOpen)
                match apparatuses[routineIndex]:
                    case Routines_conn.FXR_conn:
                        currentRoutine = FloorRoutine([],0,0,0,0,0,False,[])
                    case Routines_conn.PHR_conn:
                        currentRoutine = PommelRoutine([],0,0,0,0,0,False,[])
                    case Routines_conn.SRR_conn:
                        currentRoutine = RingsRoutine([],0,0,0,0,0,False,[])
                    case Routines_conn.VTR_conn:
                        currentRoutine = VaultRoutine([],0,0,0,0,0,False,[])
                    case Routines_conn.PBR_conn:
                        currentRoutine = PbarsRoutine([],0,0,0,0,0,False,[])
                    case Routines_conn.HBR_conn:
                        currentRoutine = HbarRoutine([],0,0,0,0,0,False,[])
                current_conn = apparatuses[routineIndex]
                cursor = current_conn.cursor()
                
                query = "SELECT * FROM " + routineToOpen
                cursor.execute(query)
                rows = cursor.fetchall()
                print(routineToOpen + " is a " + currentRoutine.apparatus + " routine.")

                i = 0
                for row in rows:
                    print(row)
                    
                    newSkill = currentRoutine.make_newSkill(row, "view")
                    currentRoutine.skills.append(newSkill)

                    currentRoutine.numberOfSkills += 1
                    
                    if currentRoutine.skills[i].eg == "I":
                        currentRoutine.hasEGI += 1
                    elif currentRoutine.skills[i].eg == "II":
                        currentRoutine.hasEGII += 1 
                    elif currentRoutine.skills[i].eg == "III":
                        currentRoutine.hasEGIII += 1
                    elif currentRoutine.skills[i].eg == "IV":
                        currentRoutine.hasEGIV += 1
                    i += 1
                currentRoutine.print_skills()
                #Does the routine meet all the requirements
                currentRoutine.validate_routine()
                if not currentRoutine.isValid:
                    print("This routine does not meet all of the FIG requirements and the D-score may be incorrect.")
                #Finds D-Score
                if currentRoutine.apparatus != "vault":
                    routineValue = currentRoutine.calculate_D_score()
                else:
                    routineValue = currentRoutine.skills[0].value                    
                print("The D-score of this routine is: " + str(routineValue))
                #else:
                    #print("Cannot calculate D-score until routine complies with FIG requirements.")
                edit = util.ReadIntegerRange("Make changes (1), Delete routine (2), Exit (3)", 1, 3)
                match edit:
                    case 1: #Allows editing of the routine
                        currentRoutine.build_routine(routineToOpen, False, Routines_conn, COP_conn)
                        self.view_routines(self, True, routineToOpen, Routines_conn, COP_conn)
                    case 2: #Deletes the routine
                        confirm = input("Are you sure you want to delete " + routineToOpen + "? (y/n) ")
                        if confirm == "y" or confirm == "Y":
                            query = "DROP TABLE " + routineToOpen
                            cursor.execute(query)

if __name__ == '__main__':
    Program.main(Program)