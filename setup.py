import json
import platform
import requests
import os
from zipfile import ZipFile
import cx_Oracle

d = json.load(open('fullDownloads.json'))['downloads']
p = platform.system().lower()
m = platform.machine()
clientHome="."
type="lite"


for version in d['platform'][p]['versions']:
    if ( version['version'] == d['platform'][p]['latest'] and version['type'] == type):
        print(version['version'])
        print(version['download'])
        print(version['type'])
        r = requests.get(version['download'])
        output =  os.path.basename(version['download'])
        with open(output, 'wb') as f:
            f.write(r.content)
            ZipFile(output).extractall(".")
        with ZipFile(output, 'r') as f:
             clientHome=os.path.dirname( f.namelist()[0])
        print(clientHome)


cx_Oracle.init_oracle_client(lib_dir=clientHome)
connection = cx_Oracle.connect(user="klrice", password="klrice",
                               dsn="localhost:1521/xe")

cursor = connection.cursor()
cursor.execute("""
        SELECT first_name, last_name
        FROM employees
        WHERE department_id = :did AND employee_id > :eid""",
        did = 50,
        eid = 190)
for fname, lname in cursor:
    print("Values:", fname, lname)