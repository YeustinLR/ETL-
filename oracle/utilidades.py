# oracle/utilidades.py

import pandas as pd
import conexion as conn
import cx_Oracle

# Conexiones a las bases de datos Oracle y SQL Server
oradbconn = conn.ora_conndb()
target_conn = conn.mssql_conndb(1)

def get_user_tables():
    """Obtiene todas las tablas de usuario en Oracle."""
    cursor = oradbconn.cursor()
    try:
        cursor.execute("SELECT table_name FROM user_tables")
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    except Exception as e:
        print(f"Error al obtener las tablas de usuario: {str(e)}")
        return None
    finally:
        cursor.close()

def get_column_definitions(table_name):
    """Obtiene las definiciones de columnas de una tabla de Oracle."""
    cursor = oradbconn.cursor()
    try:
        cursor.execute(f"""
            SELECT column_name, data_type, data_length, data_precision, data_scale
            FROM user_tab_columns
            WHERE table_name = '{table_name.upper()}'
        """)
        columns = cursor.fetchall()
        return columns
    except Exception as e:
        print(f"Error obteniendo definiciones de columnas para {table_name}: {str(e)}")
        return None
    finally:
        cursor.close()

def oracle_to_sqlserver_type(data_type, data_length, data_precision, data_scale):
    """Convierte un tipo de dato de Oracle a su equivalente en SQL Server."""
    if data_type == "VARCHAR2":
        return f"VARCHAR({data_length})"
    elif data_type == "NUMBER":
        if data_scale == 0:
            return "INT" if data_precision <= 10 else "BIGINT"
        return f"DECIMAL({data_precision}, {data_scale})"
    elif data_type == "DATE":
        return "DATETIME"
    elif data_type == "CHAR":
        return f"CHAR({data_length})"
    return "TEXT"

def create_table_if_not_exists(owner, table_name):
    """Crea una tabla en SQL Server con la estructura de la tabla de Oracle si no existe."""
    columns = get_column_definitions(table_name)
    if columns:
        sql_create = f"CREATE TABLE {owner}.{table_name}_Jardineria ("
        sql_columns = []
        for col_name, col_type, col_length, col_precision, col_scale in columns:
            sql_type = oracle_to_sqlserver_type(col_type, col_length, col_precision, col_scale)
            sql_columns.append(f"{col_name} {sql_type}")
        sql_create += ", ".join(sql_columns) + ")"

        cursor = target_conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}_Jardineria'")
            if not cursor.fetchone():
                cursor.execute(sql_create)
                target_conn.commit()
                print(f"Tabla {table_name}_Jardineria creada en SQL Server.")
            else:
                print(f"La tabla {table_name}_Jardineria ya existe en SQL Server.")
        except Exception as e:
            print(f"Error al crear la tabla {table_name}: {str(e)}")
            target_conn.rollback()
        finally:
            cursor.close()

def get_oracle_data(owner, table_name):
    """Obtiene los datos de una tabla de Oracle."""
    cursor = oradbconn.cursor()
    try:
        sql = f"SELECT * FROM {owner}.{table_name}"
        cursor.execute(sql)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(f"Error al obtener datos de Oracle: {str(e)}")
        return None
    finally:
        cursor.close()

def delete_data_entity(table, operation):
    """Limpia los datos de una tabla en SQL Server mediante DELETE o TRUNCATE."""
    cursor = target_conn.cursor()
    try:
        if operation.upper() == 'DELETE':
            cursor.execute(f"DELETE FROM {table}_Jardineria")
        elif operation.upper() == 'TRUNCATE':
            cursor.execute(f"TRUNCATE TABLE {table}_Jardineria")
        else:
            raise ValueError("Operación no válida. Use 'DELETE' o 'TRUNCATE'.")
        
        target_conn.commit()
        print(f"Operación {operation} realizada en la tabla {table}_Jardineria.")
    except Exception as e:
        print(f"Error al realizar la operación: {str(e)}")
    finally:
        cursor.close()

def add_data_entity(owner, table_name):
    """Inserta datos en una tabla de SQL Server desde una tabla de Oracle."""
    numfields = len(get_column_definitions(table_name))
    data = get_oracle_data(owner, table_name)
    if data:
        insert_sql = f"INSERT INTO dbo.{table_name}_Jardineria VALUES ({', '.join(['?' for _ in range(numfields)])})"
        target_cursor = target_conn.cursor()
        try:
            target_cursor.executemany(insert_sql, data)
            target_conn.commit()
            print(f"Datos insertados en la tabla {table_name}_Jardineria de SQL Server.")
            print("-------------------------------")
            print("")

        except Exception as e:
            print(f"Error al insertar datos en la tabla {table_name}_Jardineria: {str(e)}")
            target_conn.rollback()
        finally:
            target_cursor.close()
