from datetime import datetime
import requests
import json
import pandas as pd

current_date = datetime.now().date()
#csv_path = 'C:/Users/esau/Desktop/ITC/Código/crono/dataelementymascosas.csv'
csv_path = '/app/dataorg.csv'
illnes = pd.read_csv(csv_path)


def login():
    session = requests.Session()
    session.auth = ('admin', 'district')
    return session

# Get Info about DataSets filtered by name
def getDataSetInfoByName(name):
    """
    :param name: name used to filter in to data sets
    :return: This method return the basic information about specific dataset filtered by id
    """

    try:
        session = login()

        url = f"http://web:8080/api/dataSets.json?"
        params = {
            "filter":f"name:like:{name}"
        }
        response = session.get(url, headers={'content-type': 'application/json'}, params=params)
        #changeLog(f"[FETCHING DATA-SET INFO] >> {response.text}")
        return response.text
    except Exception as e:
        print(e)
        #changeLog("Unspected exception")
# Get Info about DataSets filtered by name
def getOrgUnitInfoByName(name):
    """
    :param name: name used to filter in to OrgUnits
    :return: This method return the basic information about specific organisation unit filtered by id
    """
    try:
        session = login()
        url = f"http://web:8080/api/organisationUnits.json?"
        params = {
            "filter": f"name:like:{name}"
        }
        response = session.get(url, headers={'content-type': 'application/json'}, params=params)
        #changeLog(f"[FETCHING ORG-UNIT INFO] >> {response.text}")
        return response.text
    except Exception as e:
        print(e)
# Get Info about DataElements filtered by name
def getDataElementInfoByName(name):
    """
    :param name: name used to filter inn to Data Elements
    :return:  This method return the basic information about specific data element filtered by id
    """
    try:
        session = login()
        url = f"http://web:8080/api/dataElements.json?"
        params = {
            "filter": f"name:like:{name}"
        }
        response = session.get(url, headers={'content-type': 'application/json'}, params=params)
        #changeLog(f"[FETCHING DATA-ELEMENT INFO] >> {response.text}")
        return response.text
    except Exception as e:
        print(e)
#changeLog("Unspected exception")
# Generate a session to makes request





def addDataValue(DataSetName:str,OrgUnitName:str,DataValueSets):

    # Getting data set id for payload
    DataSetLoaded = json.loads(getDataSetInfoByName(DataSetName))
    DataSetId = DataSetLoaded['dataSets'][0]['id']


    # Getting orgUnit id for payload
    OrgUnitLoaded = json.loads(getOrgUnitInfoByName(OrgUnitName))
    OrgUnitId = OrgUnitLoaded['organisationUnits'][0]['id']



    #changeLog(f"[PROCESSING DATA] >> " + "Converting dataelement name to data element id")
    DataValueSets_loaded = json.loads(DataValueSets)
    diccion = DataValueSets_loaded[0]

    payloads = []
    for fecha, sub_diccionario in diccion.items():
        sub_diccionario_lista = [sub_diccionario]
        payload = {
            "dataSet": DataSetId,
            "completeDate": f"{current_date.strftime('%Y-%m-%d')}",
            "period": fecha,
            "orgUnit": OrgUnitId,
            "dataValues": sub_diccionario_lista
        }
        payloads.append(payload)
    for payload in payloads:
        try:

            session = login()
            url = "http://web:8080/api/dataValueSets"
            #127.0.0.1
            response = session.post(url, json=payload, headers={'content-type': 'application/json'})
            print(payload)
            print(response.text)
        except Exception as e:
            print(e)

def add_data(pacience):
    for elementos in pacience:
        user, password, dbname, Hostname,Facility_dhis2, Orgunits, ports, Nueva_Columna = elementos
        datasetname = illnes['datasetName'][0]
        addDataValue(datasetname,Orgunits,json.dumps(Nueva_Columna))


            
