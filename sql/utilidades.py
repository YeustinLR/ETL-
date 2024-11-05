# utilidades/db_utilities.py

import pyodbc
from conexion import mssql_conndb, mssql_conndb_nort

def verificar_tabla_origen(tabla):
    """
    Verifica si la tabla de origen existe.
    """
    conexion_origen = mssql_conndb_nort()
    cursor_origen = conexion_origen.cursor()
    
    # Consulta para verificar la existencia de la tabla
    consulta_verificar = f"""
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME = '{tabla}'
    """
    cursor_origen.execute(consulta_verificar)
    existe = cursor_origen.fetchone()[0] > 0
    
    cursor_origen.close()
    conexion_origen.close()
    
    if existe:
        print(f"La tabla '{tabla}' existe en la base de datos de origen.")
    else:
        print(f"La tabla '{tabla}' no existe en la base de datos de origen.")
        print("-----------------------------------------------------")
        print(" ")
    
    return existe


def obtener_estructura_tabla_origen(tabla):
    """
    Obtiene la estructura de la tabla de origen (nombre de columna, tipo de datos, longitud y precisión).
    """
    # Conectar a la base de datos de origen
    conexion_origen = mssql_conndb_nort()  # Usa tu función de conexión
    cursor_origen = conexion_origen.cursor()
    
    # Consulta para obtener la estructura de la tabla
    consulta_estructura = f"""
    SELECT 
        COLUMN_NAME,
        DATA_TYPE,
        CASE 
            WHEN DATA_TYPE IN ('char', 'varchar', 'nchar', 'nvarchar') THEN CHARACTER_MAXIMUM_LENGTH
            WHEN DATA_TYPE IN ('binary', 'varbinary') THEN CHARACTER_MAXIMUM_LENGTH
            WHEN DATA_TYPE IN ('decimal', 'numeric') THEN NUMERIC_PRECISION
            WHEN DATA_TYPE IN ('float', 'real') THEN NUMERIC_PRECISION
            ELSE NULL
        END AS MAX_LENGTH_OR_PRECISION,
        CASE 
            WHEN DATA_TYPE IN ('decimal', 'numeric') THEN NUMERIC_SCALE
            ELSE NULL
        END AS SCALE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = '{tabla}'
    """
    
    cursor_origen.execute(consulta_estructura)
    estructura = cursor_origen.fetchall()  # Obtener todos los resultados
    
    cursor_origen.close()
    conexion_origen.close()
    
    return estructura

def obtener_datos_tabla_origen(tabla):
    """
    Obtiene todos los datos de la tabla de origen y la descripción de las columnas.
    """
    conexion_origen = mssql_conndb_nort()
    cursor_origen = conexion_origen.cursor()
    
    # Consulta para obtener todos los datos de la tabla de origen
    consulta_origen = f"SELECT * FROM {tabla}"
    cursor_origen.execute(consulta_origen)
    
    # Obtener nombres de columnas de la tabla de origen
    columnas = [desc[0] for desc in cursor_origen.description]
    
    # Obtener todas las filas de la tabla de origen
    datos = cursor_origen.fetchall()
    
    cursor_origen.close()
    conexion_origen.close()
    
    return datos, columnas  # Retornar también los nombres de las columnas


def verificar_tabla_destino(tabla):
    """
    Verifica si la tabla de destino existe.
    """
    conexion_destino = mssql_conndb()
    cursor_destino = conexion_destino.cursor()
    
    consulta_verificar = f"""
    IF OBJECT_ID('{tabla}', 'U') IS NOT NULL
        SELECT 1 AS Existe
    ELSE
        SELECT 0 AS Existe
    """
    cursor_destino.execute(consulta_verificar)
    existe = cursor_destino.fetchone()[0]
    
    cursor_destino.close()
    conexion_destino.close()
    
    return existe


def crear_tabla_destino(tabla, estructura):
    """
    Crea la tabla de destino con la estructura obtenida de la tabla de origen.
    """
    conexion_destino = mssql_conndb()
    cursor_destino = conexion_destino.cursor()
    
    columnas_definicion = []
    for columna, tipo, max_len, escala in estructura:
        if tipo in ["nchar", "nvarchar", "char", "varchar"]:  # Tipos con longitud
            if max_len is not None and max_len > 0:
                columnas_definicion.append(f"{columna} {tipo}({max_len})")
            else:
                columnas_definicion.append(f"{columna} {tipo}(max)")  # Si no hay longitud, usamos "max"
        
        elif tipo == "decimal" and max_len is not None:
            # Si hay precisión y escala, añadirlos
            columnas_definicion.append(f"{columna} {tipo}({max_len}, {escala})")
        
        elif tipo == "int":
            columnas_definicion.append(f"{columna} {tipo}")
        
        elif tipo == "float":
            columnas_definicion.append(f"{columna} {tipo}")
        
        elif tipo == "image":
            columnas_definicion.append(f"{columna} varbinary(max)")  # Cambiar image a varbinary(max)
        
        else:
            columnas_definicion.append(f"{columna} {tipo}")  # Para otros tipos no especificados
    
    if columnas_definicion:
        consulta_crear = f"CREATE TABLE {tabla} ({', '.join(columnas_definicion)})"
        print(f"Ejecutando consulta: {consulta_crear}")  # Debug: mostrar la consulta que se va a ejecutar
        cursor_destino.execute(consulta_crear)
        conexion_destino.commit()
        print(f"Tabla {tabla} creada en la base de datos de destino con la misma estructura.")
    else:
        print(f"No se pudo crear la tabla {tabla} porque la definición de columnas está vacía.")
    
    cursor_destino.close()
    conexion_destino.close()



def truncar_tabla_destino(tabla):
    """
    Limpia los datos de la tabla de destino.
    """
    conexion_destino = mssql_conndb()
    cursor_destino = conexion_destino.cursor()
    
    consulta_truncate = f"TRUNCATE TABLE {tabla}"
    cursor_destino.execute(consulta_truncate)
    conexion_destino.commit()
    print(f"Datos en la tabla {tabla} han sido limpiados.")
    
    cursor_destino.close()
    conexion_destino.close()


def insertar_datos(tabla, datos, columnas):
    """
    Inserta datos en la tabla de destino.
    """
    conexion_destino = mssql_conndb()
    cursor_destino = conexion_destino.cursor()
    
    columnas_str = ", ".join(columnas)  # Usar los nombres de las columnas que se pasaron como argumento
    for fila in datos:
        valores_placeholder = ", ".join(["?" for _ in fila])  # Genera un "?" por cada columna
        consulta_destino = f"INSERT INTO {tabla} ({columnas_str}) VALUES ({valores_placeholder})"
        cursor_destino.execute(consulta_destino, fila)  # Inserta los valores en la tabla de destino
    
    conexion_destino.commit()
    print(f"Datos insertados en la tabla {tabla} exitosamente.")
    print("-----------------------------------------------------")
    print(" ")


    
    cursor_destino.close()
    conexion_destino.close()
