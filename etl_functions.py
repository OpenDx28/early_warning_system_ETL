from collections import Counter


def rows_tolist(datos):
    lista_filas = []

    # Itera sobre cada fila del DataFrame y agrega la fila a la lista
    for indice, fila in datos.iterrows():
        lista_filas.append(fila.tolist())
    return lista_filas


def info_death(recor) :
    death = []
    print('creating death lists')
    for rec in recor:
        death.append((rec.dod, rec.cod.name))
    return death

def info_disease(record):
    confir = []
    suspe = []
    reco = []
    print('creating disease lists')
    for rec in record:
        if rec.lab_confirmed is True and rec.healed_date is None:
            confir.append((rec.diagnosed_date, rec.pathology.name))
        elif rec.lab_confirmed is False and rec.healed_date is None:
            suspe.append((rec.diagnosed_date, rec.pathology.name))
        elif rec.lab_confirmed is True and rec.healed_date is not None:
            reco.append((rec.healed_date, rec.pathology.name))
    return confir, suspe, reco

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

def new_dict(dicc_act):

    nuevo_diccionario = {}
    # Recorrer el diccionario original
    for clave, valor in dicc_act.items():
        for fecha, cantidad in valor.items():
            nuevo_diccionario[fecha] = {'dataElement': clave, 'value': cantidad}
    return nuevo_diccionario

def dict_in_list(nuevo_diccionario):
    lista = []

    lista.append(nuevo_diccionario)
    return lista

