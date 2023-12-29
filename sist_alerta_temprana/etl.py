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


bedh1,bedicu1,dish1,dispc1,ocu1,tuover1,esta1 = info_registration(reg1)
bedh2,bedicu2,dish2,dispc2,ocu2,tuover2,esta2 = info_registration(reg2)
'''
newb1,newbdied1,born1,cae1, vag1 = info_newborn(new1)
newb2,newbdied2,born2,cae2, vag2 = info_newborn(new2)

surg1,surgdied1,surgalive1, weekend_surg1,weekend_surgalive1 = info_surgery(surge1)
surg2,surgdied2,surgalive2, weekend_surg2,weekend_surgalive2 = info_surgery(surge2)


logging.info(f"info obtained from all models")
print('info obtained from all models')


morta_surgical1 = dict_in_list(dict_payload(div_ind(to_week(sorteddict(transf_dict(surgalive1))),to_week(sorteddict(transf_dict(surg1)))),resultp[0]))
morta_surgical2 = dict_in_list(dict_payload(div_ind(to_week(sorteddict(transf_dict(surgalive2))),to_week(sorteddict(transf_dict(surg2)))),resultp[0]))
logging.info(f"morta_surgical")

index_surgery1 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(surg1))),to_week(sorteddict(transf_dict(surg1)))),resulto[0]))
index_surgery2 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(surg2))),to_week(sorteddict(transf_dict(surg2)))),resulto[0]))
logging.info(f"index_surgery")

episode_surgery1 = dict_in_list(dict_payload(to_week(sorteddict(transf_dict(surg1))),resultu[0]))
episode_surgery2 = dict_in_list(dict_payload(to_week(sorteddict(transf_dict(surg1))),resultu[0]))
logging.info(f"episode_surgery")

'''
turnover1 = dict_in_list(dict_payload(div_ind(to_week(sorteddict(transf_dict(tuover1))),to_week(sorteddict(transf_dict(bedh1)))),resultx[0]))
turnover2 = dict_in_list(dict_payload(div_ind(to_week(sorteddict(transf_dict(tuover2))),to_week(sorteddict(transf_dict(bedh2)))),resultx[0]))
logging.info(f"turnover")

average1 = stay(transfor(esta1,resultz[0]),transformar_lista(tuover1,resultz[0]),resultz[0])
average2 = stay(transfor(esta2,resultz[0]),transformar_lista(tuover2,resultz[0]),resultz[0])
logging.info(f"average")
'''

weekend_surgical1 = dict_in_list(dict_payload(div_ind(res_ind(to_week(sorteddict(transf_dict(weekend_surg1))),to_week(sorteddict(transf_dict(weekend_surgalive1)))),to_week(sorteddict(transf_dict(weekend_surg1)))),results[0]))
weekend_surgical2 = dict_in_list(dict_payload(div_ind(res_ind(to_week(sorteddict(transf_dict(weekend_surg2))),to_week(sorteddict(transf_dict(weekend_surgalive2)))),to_week(sorteddict(transf_dict(weekend_surg2)))),results[0]))
logging.info(f"weekend_surgical")

cesarean_rate1 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(cae1))),to_week(sorteddict(transf_dict(born1)))),resultq[0]))
cesarean_rate2 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(cae2))),to_week(sorteddict(transf_dict(born2)))),resultq[0]))
logging.info(f"cesarean_rate")

vaginal_rate1 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(vag1))),to_week(sorteddict(transf_dict(born1)))),resultr[0]))
vaginal_rate2 = dict_in_list(dict_payload(percent_ind(to_week(sorteddict(transf_dict(vag2))),to_week(sorteddict(transf_dict(born2)))),resultr[0]))
logging.info(f"vaginal_rate")

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
b1 = dictio_to_list(resultt,weekly(sortedict(trans_dict(ocu1, names_illnes))))
b2 = dictio_to_list(resultt,weekly(sortedict(trans_dict(ocu2, names_illnes))))
logging.info(f"B")


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

hPOR1 = dict_to_list(resultb,dividir(sumar_tres_diccionarios(sortedict(trans_dict(dise1_c, names_illnes)),sortedict(trans_dict(deathill1, names_illnes)),sortedict(trans_dict(dise1_r, names_illnes))),sortedict(trans_dict(bedh1, names_illnes))))
hPOR2 = dict_to_list(resultb,dividir(sumar_tres_diccionarios(sortedict(trans_dict(dise2_c, names_illnes)),sortedict(trans_dict(deathill2, names_illnes)),sortedict(trans_dict(dise2_r, names_illnes))),sortedict(trans_dict(bedh2, names_illnes))))
logging.info(f"hPOR")

icuPOR1 = dict_to_list(resultc,dividir(sumar_tres_diccionarios(sortedict(trans_dict(dise1_c, names_illnes)),sortedict(trans_dict(deathill1, names_illnes)),sortedict(trans_dict(dise1_r, names_illnes))),sortedict(trans_dict(bedicu1, names_illnes))))
icuPOR2 = dict_to_list(resultc,dividir(sumar_tres_diccionarios(sortedict(trans_dict(dise2_c, names_illnes)),sortedict(trans_dict(deathill2, names_illnes)),sortedict(trans_dict(dise2_r, names_illnes))),sortedict(trans_dict(bedicu2, names_illnes))))
logging.info(f"icuPOR")

aHsi1 = dict_to_list(resulth,porcentaje(sumar(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(deathill1, names_illnes))),sortedict(trans_dict(dise1_c, names_illnes))))
aHsi2 = dict_to_list(resulth,porcentaje(sumar(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(deathill1, names_illnes))),sortedict(trans_dict(dise2_c, names_illnes))))
logging.info(f"aHsi")

dHsi1 = dict_to_list(resulth,dividir(sumar(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(deathill1, names_illnes))),sortedict(trans_dict(dise1_c, names_illnes))))
dHsi2 = dict_to_list(resulth,dividir(sumar(sortedict(trans_dict(dise1_r, names_illnes)),sortedict(trans_dict(deathill1, names_illnes))),sortedict(trans_dict(dise2_c, names_illnes))))
logging.info(f"dHsi")


activecases1 = dict_to_list(result5,sumar_tres_diccionarios(sortedict(trans_dict(dise1_c, names_illnes)),sortedict(trans_dict(deathill1, names_illnes)),sortedict(trans_dict(dise1_r, names_illnes))))
activecases2 = dict_to_list(result5,sumar_tres_diccionarios(sortedict(trans_dict(dise2_c, names_illnes)),sortedict(trans_dict(deathill1, names_illnes)),sortedict(trans_dict(dise2_r, names_illnes))))
logging.info(f"activecases")

PreActiveCases1 = dict_to_list(result6,sumar_tres_diccionarios(sortedict(trans_dict(dise1_c, names_illnes)),sortedict(trans_dict(deathill1, names_illnes)),sortedict(trans_dict(dise1_r, names_illnes))))
PreActiveCases2 = dict_to_list(result6,sumar_tres_diccionarios(sortedict(trans_dict(dise2_c, names_illnes)),sortedict(trans_dict(deathill1, names_illnes)),sortedict(trans_dict(dise2_r, names_illnes))))
logging.info(PreActiveCases)
'''
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
data['Nueva_Columnaa'] = [a1,a2]
data['Nueva_Columnab'] = [phc1,phc2]
data['Nueva_Columnac'] = [tb1,tb2]
data['Nueva_Columnad'] = [ti1,ti2]
data['Nueva_Columnae'] = [solved1,solved2]
data['Nueva_Columnai'] = [DailySolvedt1,DailySolvedt2]
data['Nueva_Columnaj'] = [DeathsPercentage1,DeathsPercentage2]
data['Nueva_Columnak'] = [RecoveredPercentage1,RecoveredPercentage2]
data['Nueva_Columnal'] = [aHsi1,aHsi2]
data['Nueva_Columnam'] = [dHsi1,dHsi2]
data['Nueva_Columnan'] = [hPOR1,hPOR2]
data['Nueva_Columnao'] = [icuPOR1,icuPOR2]
data['Nueva_Columnap'] = [activecases1,activecases2]
data['Nueva_Columnaq'] = [PreActiveCases1,PreActiveCases2]
data['Nueva_Columnar'] = [b1,b2]
'''
data['Nueva_Columnas'] = [vaginal_rate1,vaginal_rate2]
data['Nueva_Columnat'] = [cesarean_rate1,cesarean_rate2]
data['Nueva_Columnau'] = [weekend_surgical1,weekend_surgical2]
data['Nueva_Columnaw'] = [episode_surgery1,episode_surgery2]

#data['Nueva_Columnay'] = [turnover1,turnover2]
#data['Nueva_Columnaz'] = [average1,average2]

con_data = rows_tolist(data)