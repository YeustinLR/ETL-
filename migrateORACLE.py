# datos.py

import oracle.utilidades as utl

def migrate_from_oracle_to_sql(tabla_origen):
    # Verificamos si la tabla existe en Oracle
    tablas_oracle = utl.get_user_tables()
    if tabla_origen.upper() not in tablas_oracle:
        print(f"La tabla '{tabla_origen}' no existe en Oracle.")
        return  # Salir de la función si la tabla no existe

    # Obtener datos de la tabla de Oracle
    datos = utl.get_oracle_data("JARDINERIA", tabla_origen)

    # Verificar o crear la tabla en SQL Server si no existe
    utl.create_table_if_not_exists("dbo", tabla_origen)

    # Copiar datos de Oracle a SQL Server
    if datos:
        utl.delete_data_entity(tabla_origen, 'TRUNCATE')  # Limpiar datos previos en SQL Server
        utl.add_data_entity('JARDINERIA', tabla_origen)
    else:
        print(f"Error al obtener datos de la tabla {tabla_origen}")






