#!/usr/bin/env python
import StringIO
import datetime
import getopt
import os
import string
import sys
import time
from subprocess import PIPE, Popen
from time import time
import cx_Oracle
import CosNaming
import GCS
from omniORB import CORBA
import sqlite3
import OSR, OSR__POA

def printtable(p_table,p_header):
    if len(p_table)>0:
        col_width = [max(len(str(x)) for x in line) for line in zip(*p_table)]
        i=0
        output=''
        if not nullcheck(p_header):
            for word in p_header:
                if col_width[i]<len(str(word)):
                    col_width[i]=len(str(word))
                output+="".join(str(word).ljust(col_width[i]+3))
                i=i+1
            print output
            print "-"*len(output)

        for row in p_table:
            i=0
            output=""
            for word in row:
                output+= "".join(str(word).ljust(col_width[i]+3))
                i=i+1
            print output
    else:
        print "No Data Found to print a table"

def nullcheck(object,name=None):
    if object==None:
        if name != None:
            print "Object " + name + " is null (None)"
            return True
    else:
        return False

def getcmdstrout(auftlist):
    process = Popen(auftlist, stdout=PIPE, shell=True)
    output = process.communicate()[0]
    return output

auftstr = getcmdstrout("auftlist --osr-id osr1")
linesp = []
linetable = []
output = []
i = 0
z = 0

for line in StringIO.StringIO(auftstr.replace(" ","")):
    if "||" in line:
        linesp = line.split('||')
        linetable.append(linesp)

for i in range(len(linetable)):
    if linetable[i][3] not in [z[0] for z in output]:
         if linetable != 'Tote':
             output.append(linetable[i][3])

outputstr = "".join(str(output[1:]))
outputstr = outputstr.replace("[","")
outputstr = outputstr.replace("]","")
outputstr = outputstr.replace("'","")

query="select cl_cont_id, cl_loc_id, cl_pos"
query+=" from container_locations"
query+=" where cl_cont_id in(" + "".join(str(outputstr)) + ")"
query+=" order by cl_cont_id"


try:
    db = cx_Oracle.connect(ocfg.value().user + '/' + ocfg.value().password + '@' + ocfg.value().sid)
    cursor = db.cursor()
    cursor.execute(query)
    CL = cursor.fetchall()
    printtable(CL, ["Container","Container_Location","Container_Position"])
except cx_Oracle.DatabaseError as e:
    print "db connection failed"
    error, = e.args
    print('Error.Code = ', error.code)
    print('Error.message =', error.message)
    print('Error.offset =', error.offset)
    sys.exit(1)
