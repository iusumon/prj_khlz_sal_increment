import sqlite3
import os

#for Development Environment
img_dir = os.path.join(os.path.dirname(__file__))

#for Executable Files
#img_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'img')

class Connection:

    def __init__(self):
        pass
        #self.connect()

    def connect(self):
        #For Executable Files
        conn = sqlite3.connect('KhulnaZO.db')
        #For Development Environment 
        # conn = sqlite3.connect('d:/workspace/prj_klnz/KhulnaZO.db')
        return conn
        

