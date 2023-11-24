import logging
from proteus import config, Model
import pandas as pd
from faker import Faker
import random
import os
from datetime import datetime
from datetime import date
import requests
import string
import json
import re
from collections import defaultdict
import pandas as pd
from get_info import *
from connection import *
from etl_functions import *
import faker

current_date = datetime.now().date()
#Ruta al archivo CSV dentro del contenedor
#csv_path = 'C:/Users/esau/Desktop/ITC/Código/crono/data.csv'
csv_path = '/app/datacon.csv'
data = pd.read_csv(csv_path)

modelos = ['gnuhealth.death_certificate','gnuhealth.patient.disease']

con_data = rows_tolist(data)


all_info = all_connec(con_data,modelos)
 
records1, records2 = all_info

dea1,dise1 = records1
dea2,dise2 = records2

deat1 = info_death(dea1)

deat2 = info_death(dea2)

#dise1_c,dise1_s,dise1_r = info_disease(dise1)
#dise2_c,dise2_s,dise2_r = info_disease(dise2)

names_illnes = list(illnes['name'])
ids = list(illnes['uid'])
'''print(dise1_c)
print(dise1_s)
print(dise1_r)
print(dise2_c)
print(dise2_s)
print(dise2_r)'''


deat1_dic = trans_dict(deat1,names_illnes)
deat2_dic = trans_dict(deat2,names_illnes)
'''deat1c_dic = trans_dict(dise1_c,names_illnes)
deat2c_dic = trans_dict(dise2_c,names_illnes)
deat1s_dic = trans_dict(dise1_s,names_illnes)
deat2s_dic = trans_dict(dise2_s,names_illnes)
deat1r_dic = trans_dict(dise1_r,names_illnes)
deat2r_dic = trans_dict(dise2_r,names_illnes)'''


deat1_dic_act = dict(zip(ids, deat1_dic.values()))
deat2_dic_act = dict(zip(ids, deat2_dic.values()))
'''deat1c_dic_act = dict(zip(ids, deat1c_dic.values()))
deat2c_dic_act = dict(zip(ids, deat2c_dic.values()))
deat1s_dic_act = dict(zip(ids, deat1s_dic.values()))
deat2s_dic_act = dict(zip(ids, deat2s_dic.values()))
deat1r_dic_act = dict(zip(ids, deat1r_dic.values()))
deat2r_dic_act = dict(zip(ids, deat2r_dic.values()))'''

new_dict1 = new_dict(deat1_dic_act)
new_dict2 = new_dict(deat2_dic_act)
'''new_dict3 = new_dict(deat1c_dic_act)
new_dict4 = new_dict(deat2c_dic_act)
new_dict5 = new_dict(deat1s_dic_act)
new_dict6 = new_dict(deat2s_dic_act)
new_dict7 = new_dict(deat1r_dic_act)
new_dict8 = new_dict(deat2r_dic_act)'''


listdea1 = dict_in_list(new_dict1)
listdea2 = dict_in_list(new_dict2)
'''listdea3 = dict_in_list(new_dict3)
listdea4 = dict_in_list(new_dict4)
listdea5 = dict_in_list(new_dict5)
listdea6 = dict_in_list(new_dict6)
listdea7 = dict_in_list(new_dict7)
listdea8 = dict_in_list(new_dict8)'''


data['Nueva_Columna'] = [listdea1,listdea2]
#data['Nueva_Columna2'] = [listdea3,listdea4]
#data['Nueva_Columna3'] = [listdea5,listdea6]
#data['Nueva_Columna4'] = [listdea7,listdea8]

con_data = rows_tolist(data)