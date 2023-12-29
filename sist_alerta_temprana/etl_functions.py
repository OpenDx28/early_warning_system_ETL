from collections import Counter
import logging
from logging_utils import setup_logging
from collections import defaultdict
from datetime import datetime,timedelta

setup_logging()


def rows_tolist(datos):
    lista_filas = []
    logging.info(f"passing each row to the list")
    # Itera sobre cada fila del DataFrame y agrega la fila a la lista
    for indice, fila in datos.iterrows():
        lista_filas.append(fila.tolist())
    return lista_filas


def info_death(records):
    logging.info("Obtaining data from the death model")
    deathillnes = [(rec.dod, rec.cod.name) for rec in records]
    death = [rec.dod for rec in records]
    necropsy = [rec.dod for rec in records if rec.autopsy]

    return death, necropsy, deathillnes


def info_disease(record):
    logging.info("Obtaining data from the disease model")
    confir = [(rec.diagnosed_date, rec.pathology.name) for rec in record if rec.lab_confirmed and rec.healed_date is None]
    suspe = [(rec.diagnosed_date, rec.pathology.name) for rec in record if not rec.lab_confirmed and rec.healed_date is None]
    reco = [(rec.healed_date, rec.pathology.name) for rec in record if rec.lab_confirmed and rec.healed_date is not None]

    return confir, suspe, reco


def info_registration(recor):
    logging.info("Obtaining data from the registration model")
    bedh = [(rec.hospitalization_date, rec.admission_reason.name) for rec in recor]
    bedicu = [(rec.hospitalization_date, rec.admission_reason.name) for rec in recor if rec.icu]
    dish = [(rec.discharge_date, rec.admission_reason.name) for rec in recor if rec.state != 'hospitalized']
    dispc = [(rec.discharge_date, rec.admission_reason.name) for rec in recor if rec.discharge_reason == 'Home']
    ocu = [(rec.discharge_date, rec.admission_reason.name) for rec in recor if rec.bed.state == 'occupied']
    tuover = [(rec.hospitalization_date) for rec in recor]
    esta = [(rec.discharge_date, rec.hospitalization_date, (rec.discharge_date - rec.hospitalization_date).days) for rec
            in recor]

    return bedh, bedicu, dish, dispc,ocu,tuover,esta


def info_newborn(recor):
    logging.info("Obtaining data from the pregnancy model")
    newb = [rec.pregnancy_end_date for rec in recor if rec.pregnancy_end_result == 'live_birth']
    newbdied = [rec.pregnancy_end_date for rec in recor if rec.pregnancy_end_result != 'live_birth']
    born = [rec.pregnancy_end_date for rec in recor]
    cae = [rec.pregnancy_end_date for rec in recor if rec.perinatal[0].start_labor_mode == 'c']
    vag = [rec.pregnancy_end_date for rec in recor if rec.perinatal[0].start_labor_mode != 'c']
    
    return newb, newbdied, born, cae, vag


def info_surgery(recor):
    logging.info("Obtaining data from the surgery model")
    surg = [rec.surgery_end_date for rec in recor]
    surgdied = [rec.surgery_end_date for rec in recor if rec.clavien_dindo != 'grade1']
    surgalive = [rec.surgery_end_date for rec in recor if rec.clavien_dindo == 'grade1']
    weekend_surg = [ date for date in surg if date.weekday() in [5, 6]]
    weekend_surgalive = [ date for date in surgalive if date.weekday() in [5, 6]]
    return surg, surgdied, surgalive, weekend_surg, weekend_surgalive 


def transf_dict(surg):
    # Truncar las fechas a solo el componente de la fecha (ignorando la hora)
    fechas_sin_hora = [fecha.date() for fecha in surg]

    # Contar la frecuencia de cada fecha truncada
    frecuencia_fechas = Counter(fechas_sin_hora)

    # Convertir el resultado a un diccionario con fechas formateadas como cadenas
    diccionario_fechas = {fecha.strftime('%Y-%m-%d'): count for fecha, count in frecuencia_fechas.items()}
    return diccionario_fechas

def dict_payload(morta,result):
    nuevo_diccionario = {}

    # Recorrer el diccionario original
    for clave, valor in morta.items():
            nuevo_diccionario[clave] = {'dataElement': result, 'value': valor}
    return nuevo_diccionario

def trans_dict(muertes, lista_valores_unicos):
    # Crear un diccionario para almacenar las fechas por enfermedad
    fechas_por_enfermedad = {enf.lower(): [] for enf in lista_valores_unicos}

    # Iterar sobre los datos de muertes y agregar las fechas a la enfermedad correspondiente
    for fecha, enfermedad in muertes:
        for enf in lista_valores_unicos:
            if enf.lower() in enfermedad.lower():
                # Verificar si la fecha ya está en la lista de la enfermedad
                if fecha not in fechas_por_enfermedad[enf.lower()]:
                    # Si no está en la lista, agregarla
                    fechas_por_enfermedad[enf.lower()].append(fecha)

    # Crear un diccionario para almacenar el conteo final
    diccionario_final = {}

    # Iterar sobre cada enfermedad y sus fechas correspondientes
    for enfermedad, fechas in fechas_por_enfermedad.items():
        # Verificar si la lista de fechas está vacía
        if not fechas:
            # Si está vacía, asignar un diccionario vacío al conteo
            conteo_fechas = {}
        else:
            # Si no está vacía, contar las fechas usando Counter
            conteo_fechas = dict(Counter(map(lambda x: x.strftime('%Y-%m-%d'), fechas)))

        # Almacenar el conteo en el nuevo diccionario
        diccionario_final[enfermedad] = conteo_fechas
    return diccionario_final

def convertir_a_primer_dia_semana(fecha):
    dt = datetime.strptime(fecha, "%Y-%m-%d")
    inicio_semana = dt - timedelta(days=dt.weekday())
    return inicio_semana.strftime("%YW%U")

def weekly(ok):
    # Convertir las fechas a "YYYY-Www" y agrupar por semana
    for enfermedad, fechas in ok.items():
        fechas_convertidas = {}
        for fecha, valor in fechas.items():
            semana = convertir_a_primer_dia_semana(fecha)
            if semana in fechas_convertidas:
                fechas_convertidas[semana] += valor
            else:
                fechas_convertidas[semana] = valor
        ok[enfermedad] = fechas_convertidas
    return ok
def to_week(a):
    nuevo_diccionario = {}

    for fecha, valor in a.items():
        # Convertir la fecha a un objeto datetime
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')

        # Calcular la semana del año (ejemplo: '2014W27')
        semana_del_ano = f'{fecha_obj.year}W{fecha_obj.strftime("%U")}'
        nuevo_diccionario[semana_del_ano] = nuevo_diccionario.get(semana_del_ano, 0) + valor
    return nuevo_diccionario

def sorteddict(a):
    return dict(sorted(a.items()))

def sumar(ejemplo,ejemplo2):
    resultado = {clave: dic.copy() for clave, dic in ejemplo.items()}

    # Iterar sobre el segundo diccionario y sumar las cantidades
    for clave, dic in ejemplo2.items():
        if clave in resultado:
            for subclave, cantidad in dic.items():
                # Utilizar el método get para obtener el valor actual o 0 si la subclave no existe
                resultado[clave][subclave] = resultado[clave].get(subclave, 0) + cantidad
        else:
            # Si la clave no está en el primer diccionario, agregarla con sus subclaves y cantidades
            resultado[clave] = dict(dic)

    # Mostrar el resultado
    return resultado

def dividir(ejemplo1,ejemplo2):
# Crear una copia del primer diccionario para no modificar el original
    resultado = {clave: dic.copy() for clave, dic in ejemplo2.items()}

    # Iterar sobre el segundo diccionario y dividir las cantidades
    for clave, dic in ejemplo1.items():
        if clave in resultado:
            for subclave, cantidad in dic.items():
                # Utilizar el método get para obtener el valor actual o 1 si la subclave no existe
                divisor = resultado[clave].get(subclave, 1)
                resultado[clave][subclave] = cantidad / divisor
        else:
            # Si la clave no está en el primer diccionario, agregarla con sus subclaves y cantidades
            resultado[clave] = {subclave: cantidad for subclave, cantidad in dic.items()}

    # Mostrar el resultado
    return resultado

def porcentaje(ejemplo1,ejemplo2):
# Crear una copia del primer diccionario para no modificar el original
    resultado = {clave: dic.copy() for clave, dic in ejemplo2.items()}

    # Iterar sobre el segundo diccionario y dividir las cantidades
    for clave, dic in ejemplo1.items():
        if clave in resultado:
            for subclave, cantidad in dic.items():
                # Utilizar el método get para obtener el valor actual o 1 si la subclave no existe
                divisor = resultado[clave].get(subclave, 1)
                resultado[clave][subclave] = (cantidad / divisor)*100
        else:
            # Si la clave no está en el primer diccionario, agregarla con sus subclaves y cantidades
            resultado[clave] = {subclave: cantidad for subclave, cantidad in dic.items()}

    # Mostrar el resultado
    return resultado

def sumar_tres_diccionarios(ejemplo1, ejemplo2, ejemplo3):
    # Crear un diccionario resultado como copia superficial del primer diccionario
    resultado = {clave: dic.copy() for clave, dic in ejemplo1.items()}

    # Iterar sobre el segundo diccionario y sumar las cantidades
    for clave, dic in ejemplo2.items():
        if clave in resultado:
            for subclave, cantidad in dic.items():
                resultado[clave][subclave] = resultado[clave].get(subclave, 0) - cantidad
        else:
            resultado[clave] = dict(dic)

    # Iterar sobre el tercer diccionario y sumar las cantidades
    for clave, dic in ejemplo3.items():
        if clave in resultado:
            for subclave, cantidad in dic.items():
                resultado[clave][subclave] = resultado[clave].get(subclave, 0) - cantidad
        else:
            resultado[clave] = dict(dic)

    # Devolver el resultado
    return resultado


def transformar_lista(fechas, elemen):
    resultado = []
    contador_fechas = {}

    for fecha in fechas:
        year, week, _ = fecha.isocalendar()
        clave = f'{year}W{week:02}'

        if clave in contador_fechas:
            contador_fechas[clave] += 1
        else:
            contador_fechas[clave] = 1

        elemento_existente = next((elem for elem in resultado if clave in elem), None)

        if elemento_existente:
            elemento_existente[clave]['value'] = contador_fechas[clave]
        else:
            elemento = {clave: {'dataElement': elemen, 'value': contador_fechas[clave]}}
            resultado.append(elemento)

    return resultado


def transfor(esta,elemen):
    sorted_date_differences = sorted(esta, key=lambda x: x[0])
    accumulated_list = [(tupla[0], tupla[1], sum(item[2] for item in sorted_date_differences[:i + 1])) for i, tupla in
                        enumerate(sorted_date_differences)]
    result_list = [(tupla[0], tupla[2]) for tupla in accumulated_list]
    formatted_result_list = [(date.strftime('%YW%W'), value) for date, value in result_list]
    max_value_dict = {}

    # Calcular el valor más alto por semana
    for week, value in formatted_result_list:
        if week in max_value_dict:
            max_value_dict[week] = max(max_value_dict[week], value)
        else:
            max_value_dict[week] = value

    # Crear una nueva lista con el valor más alto por semana
    # Convertir el diccionario a la estructura deseada
    result_list = [{week: {'dataElement': elemen, 'value': float(max_value)}} for week, max_value in
                   max_value_dict.items()]

    return result_list

def stay(result_list,abc,elemen):
    resultados = []

    # Crear diccionarios para facilitar la búsqueda de fechas en ambas listas
    diccionario_lista1 = {list(d.keys())[0]: d for d in result_list}
    diccionario_lista2 = {list(d.keys())[0]: d for d in abc}

    # Obtener todas las fechas únicas
    fechas_unicas = set(diccionario_lista1.keys()).union(diccionario_lista2.keys())

    # Iterar sobre todas las fechas y calcular los resultados
    for fecha in fechas_unicas:
        valor1 = diccionario_lista1.get(fecha, {}).get(fecha, {}).get('value', 1)
        valor2 = diccionario_lista2.get(fecha, {}).get(fecha, {}).get('value', 1)

        resultado = {fecha: {'dataElement': elemen, 'value': valor1 / valor2}}
        resultados.append(resultado)
    lista_original = sorted(resultados, key=lambda x: list(x.keys())[0])
    diccionario_grande = {}

    for diccionario_pequeno in lista_original:
        diccionario_grande.update(diccionario_pequeno)


    lista_resultante = [diccionario_grande]

    lista_resultante
    return lista_resultante

def res_ind(dic1,dic2):
    # Crear un nuevo diccionario para almacenar la suma de los valores por fecha
    result_dict_solv = {}

    # Iterar sobre las fechas comunes en ambos diccionarios
    common_dates = set(dic1.keys()) & set(dic2.keys())
    for date in common_dates:
        result_dict_solv[date] = dic1[date] - dic2[date]

    # Agregar las fechas que solo están en dic1
    for date in set(dic1.keys()) - common_dates:
        result_dict_solv[date] = dic1[date]

    # Agregar las fechas que solo están en dic2
    for date in set(dic2.keys()) - common_dates:
        result_dict_solv[date] = dic2[date]
    return result_dict_solv


def percent_ind(dic1,dic2):
    # Crear un nuevo diccionario para almacenar la suma de los valores por fecha
    result_dict_solv = {}

    # Iterar sobre las fechas comunes en ambos diccionarios
    common_dates = set(dic1.keys()) & set(dic2.keys())
    for date in common_dates:
        result_dict_solv[date] = (dic1[date] / dic2[date])*100

    # Agregar las fechas que solo están en dic1
    for date in set(dic1.keys()) - common_dates:
        result_dict_solv[date] = dic1[date]

    # Agregar las fechas que solo están en dic2
    for date in set(dic2.keys()) - common_dates:
        result_dict_solv[date] = dic2[date]
    return result_dict_solv

def percentmil_ind(dic1,dic2):
    # Crear un nuevo diccionario para almacenar la suma de los valores por fecha
    result_dict_solv = {}

    # Iterar sobre las fechas comunes en ambos diccionarios
    common_dates = set(dic1.keys()) & set(dic2.keys())
    for date in common_dates:
        result_dict_solv[date] = (dic1[date] / dic2[date])*1000

    # Agregar las fechas que solo están en dic1
    for date in set(dic1.keys()) - common_dates:
        result_dict_solv[date] = dic1[date]

    # Agregar las fechas que solo están en dic2
    for date in set(dic2.keys()) - common_dates:
        result_dict_solv[date] = dic2[date]
    return result_dict_solv

def div_ind(dic1,dic2):
    # Crear un nuevo diccionario para almacenar la suma de los valores por fecha
    result_dict_solv = {}

    # Iterar sobre las fechas comunes en ambos diccionarios
    common_dates = set(dic1.keys()) & set(dic2.keys())
    for date in common_dates:
        result_dict_solv[date] = (dic1[date] / dic2[date])

    # Agregar las fechas que solo están en dic1
    for date in set(dic1.keys()) - common_dates:
        result_dict_solv[date] = dic1[date]

    # Agregar las fechas que solo están en dic2
    for date in set(dic2.keys()) - common_dates:
        result_dict_solv[date] = dic2[date]
    return result_dict_solv

def sortedict(data):
    for disease, dates in data.items():
        data[disease] = dict(sorted(dates.items()))
    return data

def accumulated(data):
    for disease, dates in data.items():
        cumulative_count = 0
        for date, count in dates.items():
            cumulative_count += count
            data[disease][date] = cumulative_count
    return data

def new_dict(dicc_act):

    nuevo_diccionario = {}
    # Recorrer el diccionario original
    for clave, valor in dicc_act.items():
        for fecha, cantidad in valor.items():
            nuevo_diccionario[fecha] = {'dataElement': clave, 'value': cantidad}
    return nuevo_diccionario


def new_dict_dupli(dicc_act):
    nuevo_diccionario = {}

    # Recorrer el diccionario original
    for enfermedad, fechas in dicc_act.items():
        for fecha, cantidad in fechas.items():
            # Crear un nuevo diccionario con la estructura deseada
            if cantidad > 0:  # Asegurarse de agregar solo las fechas con cantidad mayor a 0
                clave = f"{fecha}-{enfermedad}"
                if fecha not in nuevo_diccionario:
                    nuevo_diccionario[fecha] = [{'dataElement': enfermedad, 'value': cantidad}]
                else:
                    nuevo_diccionario[fecha].append({'dataElement': enfermedad, 'value': cantidad})

    # Convertir el diccionario final a una lista de diccionarios
    lista_final = []
    for fecha, registros in nuevo_diccionario.items():
        for registro in registros:
            lista_final.append({fecha: [registro]})

    return lista_final

def dict_in_list(nuevo_diccionario):
    lista = []

    lista.append(nuevo_diccionario)
    return lista

def dict_to_list(list_illnes,vector):
    sector = dict(zip(list_illnes, vector.values()))
    new_dict1 = new_dict_dupli(sector)
    #listdea1 = dict_in_list(new_dict1)
    return new_dict1

def new_dict_f(dicc_act):
    nuevo_diccionario = {}

    # Recorrer el diccionario original
    for enfermedad, fechas in dicc_act.items():
        for fecha, cantidad in fechas.items():
            # Crear un nuevo diccionario con la estructura deseada
            if cantidad > 0:  # Asegurarse de agregar solo las fechas con cantidad mayor a 0
                clave = f"{fecha}-{enfermedad}"
                if fecha not in nuevo_diccionario:
                    nuevo_diccionario[fecha] = [{'dataElement': enfermedad, 'value': cantidad}]
                else:
                    nuevo_diccionario[fecha].append({'dataElement': enfermedad, 'value': cantidad})

    # Convertir el diccionario final a una lista de diccionarios
    lista_final = []
    for fecha, registros in nuevo_diccionario.items():
        for registro in registros:
            lista_final.append({fecha: [registro]})

    return lista_final

def dictio_to_list(list_illnes,vector):
    sector = dict(zip(list_illnes, vector.values()))
    new_dict1 = new_dict_f(sector)
    lista_transformada = [{clave: diccionario[0]} for diccionario_con_lista in new_dict1
    for clave, diccionario in diccionario_con_lista.items()]
    listas_listas = [[elementos] for elementos in lista_transformada]
    return listas_listas

