from migrateSQL import migrar_datos
from migrateORACLE import migrate_from_oracle_to_sql
from dim_DW import insert as dim

def main():
    
# Llama a la función de migración de datos en migrateSQL.py
    # migrar_datos("Categories")
    # migrar_datos("CustomerCustomerDemo")
    # migrar_datos("CustomerDemographics")
    # migrar_datos("Customers")
    # migrar_datos("Employees")
    # migrar_datos("EmployeeTerritories")
    # migrar_datos("Order_Details")
    # migrar_datos("Orders")
    # migrar_datos("Products")
    # migrar_datos("Region")
    # migrar_datos("Shippers")
    # migrar_datos("Suppliers")
    # migrar_datos("Territories")

# Llama a la función de migración de datos en migrateORACLE.py
    # migrate_from_oracle_to_sql("CLIENTE") 
    # migrate_from_oracle_to_sql("DETALLE_PEDIDO") 
    # migrate_from_oracle_to_sql("EMPLEADO") 
    # migrate_from_oracle_to_sql("GAMA_PRODUCTO") 
    # migrate_from_oracle_to_sql("OFICINA") 
    # migrate_from_oracle_to_sql("PAGO") 
    # migrate_from_oracle_to_sql("PEDIDO") 
    # migrate_from_oracle_to_sql("PRODUCTO")

# Llama a la funcion de insertar vistas en la tablas vdim_* de BD DW
    dim.insert_DW()

if __name__ == "__main__":
    main()