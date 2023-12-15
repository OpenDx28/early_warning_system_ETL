from proteus import config, Model
import logging
from logging_utils import setup_logging

setup_logging()
  
def connect_to_gnu(user,
                   password,
                   dbname,
                   hostname,
                   port):

    health_server = 'http://' + user + ':' + password + '@' + hostname + ':' + port + '/' + dbname + '/'
    logging.info(f"trying to connect to {health_server}")

    try:

        conf = config.set_xmlrpc(health_server)
        logging.info(f"connected to {conf}")
        print(f"connected to {conf}")
        return conf
    except Exception as e:
        logging.error(f"Connection error: {str(e)}")


def all_connec(connections,modelos):
    todo = []

    for connection in connections:
        user, password, DDBB_name, Hostname, Orgunits_code, Orgunits_name, ports, dhis2_name, dhis2_port = connection
        logging.info(f"connecting to {connection}")
        connect_to_gnu(user, password, DDBB_name, Hostname, str(ports))
        records = []
        for modelo in modelos:
            logging.info(f"connecting to {modelo}")
            MyModel = Model.get(modelo)
            record = MyModel.find([])
            records.append(record)
        todo.append(records)
    return todo

