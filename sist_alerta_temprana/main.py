from etl import *
from get_info import *
from logging_utils import setup_logging

def main():
    setup_logging()
    add_data(con_data)

if __name__ == "__main__":
    main()