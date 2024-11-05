# datos/migracion.py

from sql.utilidades import (
    verificar_tabla_origen,
    obtener_estructura_tabla_origen,
    obtener_datos_tabla_origen,
    verificar_tabla_destino,
    crear_tabla_destino,
    truncar_tabla_destino,
    insertar_datos
)
def migrar_datos(tabla):
    """
    Función principal para migrar datos de la tabla especificada.
    """
    # Primero, verificar si la tabla de origen existe
    if not verificar_tabla_origen(tabla):
        print("Proceso de migración detenido.")
        return
    
    # Obtener la estructura de la tabla de origen
    estructura = obtener_estructura_tabla_origen(tabla)
    
    # Verificar si la tabla de destino existe
    if verificar_tabla_destino(tabla) == 0:
        crear_tabla_destino(tabla, estructura)
    else:
        truncar_tabla_destino(tabla)
    
    # Obtener datos de la tabla de origen y los nombres de las columnas
    datos, columnas = obtener_datos_tabla_origen(tabla)
    
    # Insertar datos en la tabla de destino
    insertar_datos(tabla, datos, columnas)
