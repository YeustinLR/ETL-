# Proyecto de Data Warehouse

Este proyecto consiste en la creación y migración de un Data Warehouse (DW) utilizando varias tecnologías y scripts. A continuación, se detalla el contenido del repositorio, así como las instrucciones para configurar y ejecutar el proyecto.
## Características Destacadas

- **Automatización del Proceso ETL**: Implementación completa del proceso de Extracción, Transformación y Carga (ETL) para garantizar la integridad y calidad de los datos.
- **Migración Multibase de Datos**: Soporte para migración de datos desde PostgreSQL a SQL Server y Oracle.
- **Configuración Flexible**: Uso de archivos de configuración `.env` para facilitar la personalización y despliegue en diferentes entornos.

## Contenido del Repositorio

- `.env`: Archivo de configuración de entorno.
- `.env_Example`: Ejemplo del archivo de configuración de entorno.
- `.git`: Carpeta de configuración de Git.
- `.gitignore`: Archivo para ignorar archivos específicos en Git.
- `A.SQL`: Script SQL para la base de datos.
- `conexion.py`: Script de conexión a la base de datos.
- `dim_DW`: Carpeta que contiene la estructura del Data Warehouse.
- `Estructura DW`: Documentación sobre la estructura del Data Warehouse.
- `main.py`: Script principal del proyecto.
- `migrateORACLE.py`: Script para migrar datos a Oracle.
- `migrateSQL.py`: Script para migrar datos a SQL Server.
- `oracle`: Carpeta que contiene archivos específicos para Oracle.
- `sql`: Carpeta que contiene varios scripts SQL.
- `stg_dim_hechos.sql`: Script SQL para la tabla de hechos del staging.
- `stg_vdim_cliente.sql`: Script SQL para la vista de dimensión cliente.
- `stg_vdim_empleado.sql`: Script SQL para la vista de dimensión empleado.
- `stg_vdim_producto.sql`: Script SQL para la vista de dimensión producto.
- `stg_vdim_transportistas.sql`: Script SQL para la vista de dimensión transportistas.
- `__pycache__`: Carpeta que contiene los archivos compilados de Python.

## Descripción del Proyecto

### Migración de Datos

El proyecto incluye la migración de datos desde una base de datos PostgreSQL a una base de datos SQL Server. Este proceso asegura que todos los datos sean transferidos correctamente y que la integridad de los datos se mantenga.

### Proceso ETL

El proceso ETL (Extract, Transform, Load) se ha implementado para garantizar que los datos extraídos de las fuentes originales sean transformados adecuadamente antes de ser cargados en el Data Warehouse. Este proceso incluye:

1. **Extracción**: Recuperación de datos de la base de datos PostgreSQL.
2. **Transformación**: Limpieza y transformación de datos según las necesidades del Data Warehouse.
3. **Carga**: Inserción de los datos transformados en la base de datos SQL Server.

## Beneficios del Proyecto

- **Mejora en la Toma de Decisiones**: Un Data Warehouse bien diseñado permite a las organizaciones tomar decisiones informadas basadas en datos precisos y actualizados.
- **Escalabilidad**: La estructura del DW está diseñada para crecer junto con las necesidades de la empresa.
- **Integridad y Calidad de Datos**: El proceso ETL asegura que los datos migrados sean consistentes y de alta calidad.

## Casos de Uso

- **Análisis de Ventas**: Agregación de datos de ventas de múltiples fuentes para análisis en profundidad.
- **Gestión de Inventario**: Seguimiento y optimización del inventario mediante datos centralizados.
- **Informes Financieros**: Creación de informes financieros precisos y actualizados.

## Requisitos

- Python 3.8 o superior
- Base de datos Oracle
- Base de datos SQL Server
- Librerías especificadas en el archivo `.env`

## Instalación y Configuración

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. **Crear un entorno virtual**

   ```bash
   python -m venv env
   source env/bin/activate   # En Windows usa `env\Scripts\activate`
   ```

3. **Instalar las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar el archivo de entorno**

   Copia el archivo `.env_Example` a `.env` y configura las variables de entorno necesarias.

5. **Ejecutar el script principal**

   ```bash
   python main.py
   ```

## Scripts Disponibles

- **conexion.py**: Proporciona la funcionalidad para conectarse a las bases de datos.
- **migrateORACLE.py**: Permite la migración de datos a una base de datos Oracle.
- **migrateSQL.py**: Permite la migración de datos a una base de datos SQL Server.

## Estructura del Data Warehouse

La estructura del Data Warehouse se encuentra documentada en la carpeta `Estructura DW`. Esta carpeta contiene diagramas y explicaciones sobre las tablas y relaciones utilizadas.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, realiza un fork del repositorio y envía un pull request con tus cambios.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

