import os

PLOTLY_USERNAME = 'a.botti'
PLOTLY_API_KEY = 'MpDq2yINla4zb0TUd7qo'

CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

#
ROOMS_DAY =['KI', 'KL', 'LR']
ROOMS_NIGHT = ['BD1', 'BD2', 'BD3', 'BS1' ,'BS2']
ROOMS = ['KL', 'BD1']
#
WEATHER_FILES = ['GTWDSY1', 'LHRDSY1', 'LWCDSY1']
FLOORS = ['GF', 'MF', 'TF']
DWELLINGS = ['P1201', 'P1202', 'P2302']

#

# COLUMN NAMES
Dcol = '@dwelling'
Ncol = '@north'
Wcol = '@weather'
Fcol = '@floor'
wwBcol = '@wwidth_B'
wwKLcol = '@wwidth_KL'
vBcol = '@vnt_B_ls'         # vBcol = '@vnt_B_m3s'
vKLcol = '@vnt_KL_ls'       # vKLcol = '@vnt_KL_m3s'
Ocol = '@c_opaque'
Gcol = '@c_glazing'

#
# ASPECT
DICT_ASPECT = {
    'P1201':'Single',
    'P1202':'Single',
    'P1203':'Dual',
    'P1204A':'Dual',
    'P1205':'Dual',
    'P2301':'Dual',
    'P2302':'Single',
    'P2303':'Dual',
    'P2304':'Dual',
    'P2401':'Single',
    }
def get_aspect_from_D(D):
    # ASPECT
    if '$' in D:
        aspect = DICT_ASPECT[D.split('_')[0].split('$')[0]]
    elif 'op' in D:
        aspect = DICT_ASPECT[D.split('_')[0].split('o')[0]]
    elif 'w' in D:
        aspect = DICT_ASPECT[D.split('_')[0].split('w')[0]]
    else:
        aspect = DICT_ASPECT[D]
    return aspect    

def get_color_from_D(D, DICT_COLOR):
    # ASPECT
    if '$' in D:
        color = DICT_COLOR[D.split('_')[0].split('$')[0]]
    elif 'op' in D:
        color = DICT_COLOR[D.split('_')[0].split('o')[0]]
    elif 'w' in D:
        color = DICT_COLOR[D.split('_')[0].split('w')[0]]
    else:
        color = DICT_COLOR[D]
    return color

#

# COLOR
DICT_COLOR = {
    'P1201':'#328674', 'P1201$B1':'#5E976E', 'P1201$B2':'#75a3a3',
    'P1202':'#5E976E',
    'P1203':'#FAA232',
    'P1204A':'#D17C20',
    'P1205':'#863D52',
    'P2301':'#D5661A',
    'P2302':'#75a3a3',
    'P2303':'#712D19',
    'P2304':'#863D52',
    'P2401':'#5E976E',
    }

colorlib_1aspect = ['#CFF09E', '#A8DBA8', '#79BD9A', '#3B8686', '#0B486B']
colorlib_2aspect = ['#774F38', '#E08E79', '#F1D4AF']
colorlib_2aspect = ['#FAD089', '#FF9C5B', '#F5634A', '#ED303C']

#

DEFAULT_COLORSCALE = [
    "#2a4858", "#265465", "#1e6172", "#106e7c", "#007b84",
    "#00898a", "#00968e", "#19a390", "#31b08f", "#4abd8c", "#64c988",
    "#80d482", "#9cdf7c", "#bae976", "#d9f271", "#fafa6e"]

#

