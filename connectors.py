import sqlite3

class Connectors:
    def __init__(self, FXR_conn=sqlite3.connect("Databases\\FX_Routines.db"),
                PHR_conn=sqlite3.connect("Databases\\PH_Routines.db"),
                SRR_conn=sqlite3.connect("Databases\\SR_Routines.db"),
                VTR_conn=sqlite3.connect("Databases\\VT_Routines.db"),
                PBR_conn=sqlite3.connect("Databases\\PB_Routines.db"),
                HBR_conn=sqlite3.connect("Databases\\HB_Routines.db")):
        self.FXR_conn = FXR_conn
        self.PHR_conn = PHR_conn
        self.SRR_conn = SRR_conn
        self.VTR_conn = VTR_conn
        self.PBR_conn = PBR_conn
        self.HBR_conn = HBR_conn

