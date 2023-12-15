from get_info import *
from connection import *
from etl_functions import *

setup_logging()

current_date = datetime.now().date()
#Ruta al archivo CSV dentro del contenedor
csv_path = '/app/sist_alerta_temprana/datacon.csv'
data = pd.read_csv(csv_path)

modelos = ['gnuhealth.death_certificate','gnuhealth.patient.disease',
           'gnuhealth.inpatient.registration', 'gnuhealth.patient.pregnancy',
           'gnuhealth.surgery']

con_data = rows_tolist(data)


all_info = all_connec(con_data,modelos)

records1, records2 = all_info

dea1,dise1,reg1,new1,surge1 = records1
dea2,dise2,reg2,new2,surge2 = records2
logging.info(f"connecting records")
print('connecting records')


deat1,necropsy1,deathill1 = info_death(dea1)
deat2,necropsy2,deathill2 = info_death(dea2)

'''
dise1_c,dise1_s,dise1_r = info_disease(dise1)
dise2_c,dise2_s,dise2_r = info_disease(dise2)


bedh1,bedicu1,dish1,dispc1 = info_registration(reg1)
bedh2,bedicu2,dish2,dispc2 = info_registration(reg2)
'''
newb1, newbdied1,born1 = info_newborn(new1)
newb2,newbdied2,born2= info_newborn(new2)

surg1,surgdied1,surgalive1 = info_surgery(surge1)
surg2,surgdied2,surgalive2 = info_surgery(surge2)


logging.info(f"info obtained from all models")
print('info obtained from all models')


morta_surgical1 = dict_in_list(dict_payload(div_ind(to_week(sorteddict(transf_dict(surgalive1))),to_week(sorteddict(transf_dict(surg1)))),resultp[0]))
morta_surgical2 = dict_in_list(dict_payload(div_ind(to_week(sorteddict(transf_dict(surgalive2))),to_week(sorteddict(transf_dict(surg2)))),resultp[0]))
logging.info(f"morta_surgical")

index_surgery1 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(surg1))),to_week(sorteddict(transf_dict(surg1)))),resulto[0]))
index_surgery2 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(surg2))),to_week(sorteddict(transf_dict(surg2)))),resulto[0]))
logging.info(f"index_surgery")


newborn_rate1 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(newb1))),to_week(sorteddict(transf_dict(born1)))),resultn[0]))
newborn_rate2 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(newb2))),to_week(sorteddict(transf_dict(born2)))),resultn[0]))
logging.info(f"newborn_rate")

autopsy_rate1 = dict_in_list(dict_payload(percentmil_ind(to_week(sorteddict(transf_dict(necropsy1))),to_week(sorteddict(transf_dict(deat1)))),resultm[0]))
autopsy_rate2 = dict_in_list(dict_payload(percentmil_ind(to_week(sorteddict(transf_dict(necropsy2))),to_week(sorteddict(transf_dict(deat2)))),resultm[0]))
logging.info(f"autopsy_rate")

gross_mortality1 = dict_in_list(dict_payload(percentmil_ind(to_week(sorteddict(transf_dict(deat1))),to_week(sorteddict(transf_dict(deat1)))),resultl[0]))
gross_mortality2 = dict_in_list(dict_payload(percentmil_ind(to_week(sorteddict(transf_dict(deat2))),to_week(sorteddict(transf_dict(deat2)))),resultl[0]))
logging.info(f"gross_mortality")


DailyDeath1 = dictio_to_list(result1,trans_dict(deathill1, names_illnes))
DailyDeath2 = dictio_to_list(result1,trans_dict(deathill2, names_illnes))
logging.info(f"DailyDeath")

d1 = dictio_to_list(resultj,weekly(sortedict(trans_dict(deathill1, names_illnes))))
d2 = dictio_to_list(resultj,weekly(sortedict(trans_dict(deathill2, names_illnes))))
logging.info(f"D")

'''

DailyConfirmedt1 = dictio_to_list(result2,trans_dict(dise1_c, names_illnes))
DailyConfirmedt2 = dictio_to_list(result2,trans_dict(dise2_c, names_illnes))
logging.info(f"DailyConfirmed")

c1 = dictio_to_list(resultcon,weekly(sortedict(trans_dict(dise1_c, names_illnes))))
c2 = dictio_to_list(resultcon,weekly(sortedict(trans_dict(dise2_c, names_illnes))))
logging.info(f"C")

DailyRecoveredt1 = dictio_to_list(result3,trans_dict(dise1_r, names_illnes))
DailyRecoveredt2 = dictio_to_list(result3,trans_dict(dise2_r, names_illnes))
logging.info(f"DailyRecovered")

r1 = dictio_to_list(resultk,weekly(sortedict(trans_dict(dise1_r, names_illnes))))
r2 = dictio_to_list(resultk,weekly(sortedict(trans_dict(dise2_r, names_illnes))))
logging.info(f"R")

s1 = dictio_to_list(resulti,weekly(sortedict(trans_dict(dise1_s, names_illnes))))
s2 = dictio_to_list(resulti,weekly(sortedict(trans_dict(dise2_s, names_illnes))))
logging.info(f"S")

a1 = dict_to_list(resultd,weekly(sortedict(trans_dict(dish1, names_illnes))))
a2 = dict_to_list(resultd,weekly(sortedict(trans_dict(dish2, names_illnes))))
logging.info(f"A")

phc1 = dict_to_list(resulte,weekly(sortedict(trans_dict(dispc1, names_illnes))))
phc2 = dict_to_list(resulte,weekly(sortedict(trans_dict(dispc2, names_illnes))))
logging.info(f"PHC")

tb1 = dict_to_list(resultf,weekly(sortedict(trans_dict(bedh1, names_illnes))))
tb2 = dict_to_list(resultf,weekly(sortedict(trans_dict(bedh2, names_illnes))))
logging.info(f"TB")

ti1 = dict_to_list(resultg,weekly(sortedict(trans_dict(bedicu1, names_illnes))))
ti2 = dict_to_list(resultg,weekly(sortedict(trans_dict(bedicu2, names_illnes))))
logging.info(f"TI")

solved1 = dict_to_list(resulth,sumar(weekly(sortedict(trans_dict(dise1_r, names_illnes))),weekly(sortedict(trans_dict(deathill1, names_illnes)))))
solved2 = dict_to_list(resulth,sumar(weekly(sortedict(trans_dict(dise2_r, names_illnes))),weekly(sortedict(trans_dict(deathill2, names_illnes)))))
logging.info(f"Solved")

DailySolvedt1 = dict_to_list(result4,sumar(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(deathill1, names_illnes))))
DailySolvedt2 = dict_to_list(result4,sumar(sortedict(trans_dict(dise2_r, names_illnes)),sortedict(trans_dict(deathill2, names_illnes))))
logging.info(f"DailySolved")

DeathsPercentage1 = dict_to_list(resulth,porcentaje(sortedict(trans_dict(deathill1, names_illnes)),sortedict(trans_dict(dise1_c, names_illnes))))
DeathsPercentage2 = dict_to_list(resulth,porcentaje(sortedict(trans_dict(deathill2, names_illnes)),sortedict(trans_dict(dise2_c, names_illnes))))
logging.info(f"DeathsPercentage")

RecoveredPercentage1 = dict_to_list(resulth,porcentaje(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(dise1_c, names_illnes))))
RecoveredPercentage2 = dict_to_list(resulth,porcentaje(sortedict(trans_dict(dise2_r, names_illnes)),sortedict(trans_dict(dise2_c, names_illnes))))
logging.info(f"RecoveredPercentage")

aHsi1 = dict_to_list(resulth,porcentaje(sumar(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(deathill1, names_illnes))),sortedict(trans_dict(dise1_c, names_illnes))))
aHsi2 = dict_to_list(resulth,porcentaje(sumar(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(deathill1, names_illnes))),sortedict(trans_dict(dise2_c, names_illnes))))
logging.info(f"aHsi")

dHsi1 = dict_to_list(resulth,dividir(sumar(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(deathill1, names_illnes))),sortedict(trans_dict(dise1_c, names_illnes))))
dHsi2 = dict_to_list(resulth,dividir(sumar(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(deathill1, names_illnes))),sortedict(trans_dict(dise2_c, names_illnes))))
logging.info(f"dHsi")
'''

#activecases = three_dicts(conf_daily,dea_daily,recu_daily)
#activecases2 = three_dicts(conf_daily2,dea_daily2,recu_daily2)

#l1 = [morta_surgical1,index_surgery1,newborn_rate1,autopsy_rate1,gross_mortality1,DailyDeath1,d1,DailyConfirmedt1,c1,
#      DailyRecoveredt1,r1,s1,a1,phc1,tb1,ti1,solved1,DailySolvedt1,DeathsPercentage1,RecoveredPercentage1,aHsi1,dHsi1]

#l2 = [morta_surgical2,index_surgery2,newborn_rate2,autopsy_rate2,gross_mortality2,DailyDeath2,d2,DailyConfirmedt2,c2,
#      DailyRecoveredt2,r2,s2,a2,phc2,tb2,ti2,solved2,DailySolvedt2,DeathsPercentage2,RecoveredPercentage2,aHsi2,dHsi2]
print('list calculated')
'''
'''
data['Nueva_Columna'] = [morta_surgical1,morta_surgical2]
data['Nueva_Columna2'] = [index_surgery1,index_surgery2]
data['Nueva_Columna3'] = [newborn_rate1,newborn_rate2]

data['Nueva_Columna4'] = [autopsy_rate1,autopsy_rate2]
data['Nueva_Columna5'] = [gross_mortality1,gross_mortality2]
'''
data['Nueva_Columna6'] = [s1,s2]
data['Nueva_Columna7'] = [c1,c2]
data['Nueva_Columna9'] = [r1,r2]
data['Nueva_Columnaf'] = [DailyConfirmedt1,DailyConfirmedt2]
data['Nueva_Columnah'] = [DailyRecoveredt1,DailyRecoveredt2]
'''
data['Nueva_Columna8'] = [d1,d2]
data['Nueva_Columnag'] = [DailyDeath1,DailyDeath2]
'''
data['Nueva_Columna9'] = [r1,r2]
data['Nueva_Columnaa'] = [a1,a2]
data['Nueva_Columnab'] = [phc1,phc2]
data['Nueva_Columnac'] = [tb1,tb2]
data['Nueva_Columnad'] = [ti1,ti2]
data['Nueva_Columnae'] = [solved1,solved2]
data['Nueva_Columnaf'] = [DailyConfirmedt1,DailyConfirmedt2]

data['Nueva_Columnag'] = [DailyDeath1,DailyDeath2]

data['Nueva_Columnah'] = [DailyRecoveredt1,DailyRecoveredt2]
data['Nueva_Columnai'] = [DailySolvedt1,DailySolvedt2]
data['Nueva_Columnaj'] = [DeathsPercentage1,DeathsPercentage2]
data['Nueva_Columnak'] = [RecoveredPercentage1,RecoveredPercentage2]
data['Nueva_Columnal'] = [aHsi1,aHsi2]
data['Nueva_Columnan'] = [dHsi1,dHsi2]
'''

con_data = rows_tolist(data)