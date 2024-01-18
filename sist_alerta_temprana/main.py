from etl import *
from get_info import *
from logging_utils import setup_logging

PATH = ""
# PATH = "/home/paula/Documentos/opendx28/early_warning_system_ETL/sist_alerta_temprana/"

def main():
    setup_logging()
    add_data(con_data)

if __name__ == "__main__":
    main()
