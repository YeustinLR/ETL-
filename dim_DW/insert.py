import os
import pyodbc
from conexion import mssql_conndb, mssql_conndb_DW  # Importa las funciones de conexión desde tu archivo conexion.py

#------------------------------Obtener datos----------------------------------|
def obtener_datos_vdim_cliente():
    try:
        # Conectar a la base de datos STG
        conn_stg = mssql_conndb()  # Usa la función de conexión de STG
        cursor_stg = conn_stg.cursor()

        # Consulta para obtener los datos de la vista
        consulta = """
        SELECT Cliente_ID, 
           Nombre_Cliente, 
           Pais,
           Ciudad, 
           Codigo_Postal,
           Telefono, 
           Contacto,
           Region, 
           Direccion  
        FROM dbo.vdim_cliente
        """
        cursor_stg.execute(consulta)
        filas = cursor_stg.fetchall()

        # Cerrar la conexión a STG
        cursor_stg.close()
        conn_stg.close()

        return filas

    except pyodbc.Error as e:
        print(f"Error al obtener los datos de vdim_cliente: {e}")
        return []

def obtener_datos_vdim_empleado():
    try:
        # Conectar a la base de datos STG
        conn_stg = mssql_conndb()  # Usa la función de conexión de STG
        cursor_stg = conn_stg.cursor()

        # Consulta para obtener los datos de la vista
        consulta = """
        SELECT empleado_id, 
               nombre_empleado, 
               puesto,
               fecha_contratacion, 
               pais,
               ciudad, 
               jefatura,
               salario
        FROM dbo.vdim_empleado
        """
        cursor_stg.execute(consulta)
        filas = cursor_stg.fetchall()

        # Cerrar la conexión a STG
        cursor_stg.close()
        conn_stg.close()

        return filas

    except pyodbc.Error as e:
        print(f"Error al obtener los datos de vdim_empleado: {e}")
        return []

def obtener_datos_vdim_producto():
    try:
        # Conectar a la base de datos STG
        conn_stg = mssql_conndb()  # Usa la función de conexión de STG
        cursor_stg = conn_stg.cursor()

        # Consulta para obtener los datos de la vista
        consulta = """
        SELECT product_id, 
               nombre_producto, 
               categoria,
               cantidad_por_unidad, 
               precio_unitario,
               unidades_en_stock
        FROM dbo.vdim_producto
        """
        cursor_stg.execute(consulta)
        filas = cursor_stg.fetchall()

        # Cerrar la conexión a STG
        cursor_stg.close()
        conn_stg.close()

        return filas

    except pyodbc.Error as e:
        print(f"Error al obtener los datos de vdim_producto: {e}")
        return []

def obtener_datos_vdim_transportista():
    try:
        # Conectar a la base de datos STG
        conn_stg = mssql_conndb()  # Usa la función de conexión de STG
        cursor_stg = conn_stg.cursor()

        # Consulta para obtener los datos de la vista
        consulta = """
        SELECT transportista_id, 
               nombre_transportista,
               telefono 
        FROM dbo.vdim_transportista
        """
        cursor_stg.execute(consulta)
        filas = cursor_stg.fetchall()

        # Cerrar la conexión a STG
        cursor_stg.close()
        conn_stg.close()

        return filas

    except pyodbc.Error as e:
        print(f"Error al obtener los datos de vdim_transportista: {e}")
        return []


#------------------------------Insertar datos----------------------------------|
def insertar_datos_dim_cliente(filas):
    try:
        # Conectar a la base de datos DW
        conn_dw = mssql_conndb_DW()  # Usa la función de conexión de DW
        cursor_dw = conn_dw.cursor()

        # Consulta para insertar los datos en la tabla dim_cliente
        insert_query = """
        INSERT INTO dim_cliente (cliente_id, nombre_cliente, pais, ciudad, codigo_postal, telefono, asesor, region, direccion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Insertar los datos fila por fila
        for fila in filas:
            cursor_dw.execute(insert_query, fila.Cliente_ID, fila.Nombre_Cliente, fila.Pais, fila.Ciudad,
                              fila.Codigo_Postal, fila.Telefono, fila.Contacto, fila.Region, fila.Direccion)

        # Hacer commit para guardar los cambios
        conn_dw.commit()

        # Cerrar la conexión a DW
        cursor_dw.close()
        conn_dw.close()

    except pyodbc.Error as e:
        print(f"Error al insertar los datos en dim_cliente: {e}")

def insertar_datos_dim_empleado(filas):
    try:
        # Conectar a la base de datos DW
        conn_dw = mssql_conndb_DW()  # Usa la función de conexión de DW
        cursor_dw = conn_dw.cursor()

        # Consulta para insertar los datos en la tabla dim_empleado
        insert_query = """
        INSERT INTO dim_empleado (employee_id, nombre_empleado, puesto, fecha_contratacion, pais, ciudad, jefatura, salario)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Insertar los datos fila por fila
        for fila in filas:
            cursor_dw.execute(insert_query, fila.empleado_id, fila.nombre_empleado, fila.puesto, fila.fecha_contratacion,
                              fila.pais, fila.ciudad, fila.jefatura, fila.salario)

        # Hacer commit para guardar los cambios
        conn_dw.commit()

        # Cerrar la conexión a DW
        cursor_dw.close()
        conn_dw.close()

    except pyodbc.Error as e:
        print(f"Error al insertar los datos en dim_empleado: {e}")

def insertar_datos_dim_producto(filas):
    try:
        # Conectar a la base de datos DW
        conn_dw = mssql_conndb_DW()  # Usa la función de conexión de DW
        cursor_dw = conn_dw.cursor()

        # Consulta para insertar los datos en la tabla dim_producto
        insert_query = """
        INSERT INTO dim_producto (product_id, nombre_producto, categoria, cantidad_por_unidad, precio_unitario, unidades_en_stock)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        # Insertar los datos fila por fila
        for fila in filas:
            cursor_dw.execute(insert_query, fila.product_id, fila.nombre_producto, fila.categoria, fila.cantidad_por_unidad,
                              fila.precio_unitario, fila.unidades_en_stock)

        # Hacer commit para guardar los cambios
        conn_dw.commit()

        # Cerrar la conexión a DW
        cursor_dw.close()
        conn_dw.close()

    except pyodbc.Error as e:
        print(f"Error al insertar los datos en dim_producto: {e}")

def insertar_datos_dim_transportista(filas):
    try:
        # Conectar a la base de datos DW
        conn_dw = mssql_conndb_DW()  # Usa la función de conexión de DW
        cursor_dw = conn_dw.cursor()

        # Consulta para insertar los datos en la tabla dim_transportista
        insert_query = """
        INSERT INTO dim_transportista (transportista_id, nombre_transportista, telefono)
        VALUES (?, ?, ?)
        """

        # Insertar los datos fila por fila
        for fila in filas:
            cursor_dw.execute(insert_query, fila.transportista_id, fila.nombre_transportista, fila.telefono)

        # Hacer commit para guardar los cambios
        conn_dw.commit()

        # Cerrar la conexión a DW
        cursor_dw.close()
        conn_dw.close()

    except pyodbc.Error as e:
        print(f"Error al insertar los datos en dim_transportista: {e}")

#------------------------------GET----------------------------------|

def insert_DW():
    try:
        # Obtener y transferir los datos de cada vista en STG
        # Cliente
        filas_cliente = obtener_datos_vdim_cliente()
        if filas_cliente:
            insertar_datos_dim_cliente(filas_cliente)
            print("Datos de cliente transferidos exitosamente de STG a DW.")
        else:
            print("No se encontraron datos en la vista vdim_cliente.")
        
        # Empleado
        filas_empleado = obtener_datos_vdim_empleado()
        if filas_empleado:
            insertar_datos_dim_empleado(filas_empleado)
            print("Datos de empleado transferidos exitosamente de STG a DW.")
        else:
            print("No se encontraron datos en la vista vdim_empleado.")
        
        # Producto
        filas_producto = obtener_datos_vdim_producto()
        if filas_producto:
            insertar_datos_dim_producto(filas_producto)
            print("Datos de producto transferidos exitosamente de STG a DW.")
        else:
            print("No se encontraron datos en la vista vdim_producto.")
        
        # Transportista
        filas_transportista = obtener_datos_vdim_transportista()
        if filas_transportista:
            insertar_datos_dim_transportista(filas_transportista)
            print("Datos de transportista transferidos exitosamente de STG a DW.")
        else:
            print("No se encontraron datos en la vista vdim_transportista.")
    
    except Exception as e:
        print(f"Se produjo un error durante el proceso de transferencia: {e}")


