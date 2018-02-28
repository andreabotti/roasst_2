import os
from eppy import modeleditor
from eppy.modeleditor import IDF       #superseded by the import line below
import sqlite3


# Energyplus dictionary
iddfile = 'C:/EnergyPlusV8-5-0/Energy+.idd'
IDF.setiddname(iddfile)

#####
def create_html_log(output):
    f = open(output,'w')
    lines = """<html>
    <head><b>ROASST Simulation Results</b></head>
    </html>"""
    f.write(lines)
    f.close()
def append_to_html_log(output, line):
    f = open(output,'a+')
    f.write(line)
    f.close()
#####
MAIN_FOLDER_0 = 'C:/ROAST/'
MAIN_FOLDER_1 = 'C:/ROASST_1/'
MAIN_FOLDER_2 = 'C:/ROASST_2/'
MAIN_FOLDER = MAIN_FOLDER_2

#####
HTML_OUTPUT = os.path.join(MAIN_FOLDER,'2_SIMRES/','SimRes.html')
# create_html_log(HTML_OUTPUT)
#####

MAIN_FOLDER_JEPLUS  = os.path.join(MAIN_FOLDER, '2_JEPLUS_JESS')
SAP_FOLDER = os.path.join(MAIN_FOLDER_JEPLUS, 'SAP_P')
#
SIM_OUT_PATH_JEPLUS = os.path.join(MAIN_FOLDER,'2_SIMRES/JEPLUS/')
SIM_OUT_PATH_JESS = os.path.join(MAIN_FOLDER,'2_SIMRES/JESS/')
#####

ROOMS_DAY = ['KI', 'KL', 'LR']
ROOMS_NIGHT = ['BD1', 'BD2', 'BD3', 'BS1' ,'BS2']
#

WEATHER_FILES = ['GTWDSY1', 'LHRDSY1', 'LWCDSY1']

FLOORS = ['GF', 'MF', 'TF']
FLOORS = ['MF']


UNITS = ['P1201', 'P1201$BKL.D15','P1201$BW.D15'] + ['P1202', 'P1202$BKL.D15','P1202$BW.D15']
UNITS = ['P1201','P1202']
UNITS = ['P1201','P1202','P1203', 'P1204A', 'P2301','P2302','P2303','P2304']
#####
