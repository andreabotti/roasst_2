import os

PLOTLY_USERNAME = 'a.botti'
PLOTLY_API_KEY = 'MpDq2yINla4zb0TUd7qo'

CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER_PATH = CURRENT_DIR_PATH + '/data'


#
MAIN_FOLDER = 'C:/ROASST_3/'
ALL_PROJECTS_FOLDER = os.path.join(MAIN_FOLDER, 'JEPLUS_PROJECTS')
SAP_FOLDER = os.path.join(ALL_PROJECTS_FOLDER, 'SAP_P')
ROOMS_DAY =['KI', 'KL', 'LR']
ROOMS_NIGHT = ['BD1', 'BD2', 'BD3', 'BS1' ,'BS2']
#
WEATHER_FILES = ['GTWDSY1', 'LHRDSY1', 'LWCDSY1']
#
FLOORS = ['GF', 'MF', 'TF']
# FLOORS = ['MF']
#
# DWELLINGS = ['P1201', 'P1201$BKL.D15','P1201$BW.D15'] + ['P1202', 'P1202$BKL.D15','P1202$BW.D15']
DWELLINGS = ['P1201','P1202','P1203', 'P1204A', 'P2301','P2302','P2303','P2304']
DWELLINGS = ['P2302']
#
ROOMS = ['KL', 'BD1']

#
DICT_ASPECT = {
    'P1201':'Single','P1201$B1':'Single','P1201$B2':'Single',
    'P1202':'Single',
    'P1203':'Dual',
    'P1204A':'Dual',
    'P2301':'Dual',
    'P2302':'Single',
    'P2303':'Dual',
    'P2304':'Dual',
    }

#
# sim_choice, SIM_JOBS = 'JEPLUS', 8
sim_choice, SIM_JOBS = 'JESS', 24
#
SIM_OUT_PATH_JEPLUS = os.path.join(MAIN_FOLDER,'SIMRES/JEPLUS/')
SIM_OUT_PATH_JESS = os.path.join(MAIN_FOLDER,'SIMRES/JESS/')
#
if sim_choice == 'JEPLUS':
    SIM_OUT_PATH = SIM_OUT_PATH_JEPLUS
if sim_choice == 'JESS':
    SIM_OUT_PATH = SIM_OUT_PATH_JESS


# COLUMN NAMES
Dcol = '@dwelling'
Ncol = '@north'
Wcol = '@weather'
Fcol = '@floor'
wwBcol = '@wwidth_B'
wwKLcol = '@wwidth_KL'
vBcol = '@vnt_B_m3s'
vKLcol = '@vnt_KL_m3s'
Ocol = '@c_opaque'
Gcol = '@c_glazing'