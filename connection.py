from proteus import config, Model


    
def connect_to_gnu(user,
                   password,
                   dbname,
                   hostname,
                   port):
    '''user = "admin"
    dbname = "ghs"
    hostname = 'test1.medtec4susdev.org'
    port = ""
    password = "opendx28"
    '''
    health_server = 'http://' + user + ':' + password + '@' + hostname + ':' + port + '/' + dbname + '/'
    print(f"trying to connect to {health_server}")

    try:

        conf = config.set_xmlrpc(health_server)

        print(conf)

        print(f"connected to conf")
        return conf
    except Exception as e:
        print(f"Connection error: {str(e)}")


def all_connec(connections,modelos):
    todo = []

    for connection in connections:
        user, password, dbname, hostname, id, hospital_name, port = connection
        print(connection)
        connect_to_gnu(user, password, dbname, hostname, str(port))
        records = []
        for modelo in modelos:
            MyModel = Model.get(modelo)
            record = MyModel.find([])
            records.append(record)
        todo.append(records)
    return todo

