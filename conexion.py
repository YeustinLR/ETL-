# conexion.py

import os
import pyodbc
import cx_Oracle
from dotenv import load_dotenv

load_dotenv()

def mssql_conndb(method=1):
    server = os.getenv('DB_SERVER') # BD de STG
    database = os.getenv('DB_DATABASE')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    if not password:
        raise ValueError("La variable de entorno DB_PASSWORD no está definida.")

    if method == 1:
        conexion_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conexion = pyodbc.connect(conexion_str)
        
    return conexion

def ora_conndb():
    cx_Oracle.init_oracle_client(lib_dir=os.getenv('ORACLE_CLIENT_DIR'))
    server = os.getenv('ORA_SERVER')
    database = os.getenv('ORA_DATABASE')
    username = os.getenv('ORA_USERNAME')
    password = os.getenv('ORA_PASSWORD')
    
    if not password:
        raise ValueError("La variable de entorno ORA_PASSWORD no está definida.")

    connection = cx_Oracle.connect(user=username, password=password, dsn=f"{server}/{database}")
    return connection

def mssql_conndb_nort():
    server = os.getenv('DB_Nort_SERVER') #BD de Northwind
    database = os.getenv('DB_Nort_DATABASE')
    username = os.getenv('DB_Nort_USERNAME')
    password = os.getenv('DB_Nort_PASSWORD')

    if not password:
        raise ValueError("La variable de entorno DB_DEST_PASSWORD no está definida.")

    conexion_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conexion = pyodbc.connect(conexion_str)
    
    return conexion

def mssql_conndb_DW():
    server = os.getenv('DB_DW_SERVER') #BD de DW
    database = os.getenv('DB_DW_DATABASE')
    username = os.getenv('DB_DW_USERNAME')
    password = os.getenv('DB_DW_PASSWORD')

    if not password:
        raise ValueError("La variable de entorno DB_DEST_PASSWORD no está definida.")

    conexion_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conexion = pyodbc.connect(conexion_str)
    
    return conexion
