
--CREAR VISTA vdim_cliente en BD STAGING
CREATE  VIEW vdim_cliente AS
SELECT	[Cliente_ID]
		,[Nombre_Cliente]
		,[Telefono]
		,[Direccion]
		,[Ciudad]
		,[Region]
		,[Codigo_Postal]
		,[Pais]
		,[Contacto]

FROM ( 
SELECT
    C.CustomerID AS Cliente_ID,
    C.CompanyName AS Nombre_Cliente,
    C.Phone AS Telefono,
    C.Address AS Direccion,
    C.City AS Ciudad,
    C.Region AS Region,
    C.PostalCode AS Codigo_Postal,
    C.Country AS Pais,
	C.ContactName AS Contacto

FROM
    Customers AS C

UNION

SELECT
    CAST(J.CODIGO_CLIENTE AS varchar(10)) AS Cliente_ID,
    J.NOMBRE_CLIENTE AS Nombre_Cliente,
    J.TELEFONO AS Telefono,
    J.LINEA_DIRECCION1 AS Direccion,
    J.CIUDAD AS Ciudad,
    J.REGION AS Region,
    J.CODIGO_POSTAL AS Codigo_Postal,
    J.Pais AS Pais,
	J.NOMBRE_CONTACTO AS Contacto

FROM
    CLIENTE_Jardineria AS J
) AS V;

SELECT * FROM vdim_cliente;

-----------------------Transformacion
-----------------------
ALTER VIEW vdim_cliente AS
SELECT 
    [Cliente_ID],
    [Nombre_Cliente],
    [Telefono],  -- No alteramos la columna Telefono
    [Direccion], -- No alteramos la columna Direccion
    [Ciudad],    -- No alteramos la columna Ciudad
    [Region],
    [Codigo_Postal],
    [Pais],
    [Contacto]   -- No alteramos la columna Contacto
FROM (
    -- Datos de la tabla CLIENTE_Jardineria con normalización
    SELECT 
        CAST(CODIGO_CLIENTE AS VARCHAR(10)) AS [Cliente_ID],
        NOMBRE_CLIENTE,
        TELEFONO,  -- No alteramos Telefono
        CIUDAD AS Ciudad,  -- No alteramos Ciudad
        CASE
            WHEN Region IS NULL THEN 'Sin informacion'
            ELSE Region
        END AS Region,
        CASE
            WHEN LEN(CODIGO_POSTAL) < 5 THEN RIGHT('00000' + CODIGO_POSTAL, 5)
            ELSE CODIGO_POSTAL
        END AS Codigo_Postal,
        UPPER(CASE 
            WHEN PAIS = 'UK' THEN 'United Kingdom'
            WHEN PAIS = 'USA' THEN 'United States'
            ELSE PAIS
        END) AS Pais,		-- Normalización de la calles
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(LINEA_DIRECCION1, 'C/', 'Calle '),
                'Av.', 'Avenida '),
            'Rda.', 'Ronda '),
        'Plza.', 'Plaza ') AS Direccion,
        NOMBRE_CONTACTO AS Contacto -- No alteramos Contacto
    FROM CLIENTE_Jardineria

    UNION ALL -- Usamos UNION ALL para mantener todos los registros sin eliminar duplicados

    -- Datos de la tabla Customers con normalización de ciertos campos
    SELECT 
        CUSTOMERID AS Cliente_ID,
        CompanyName AS Nombre_Cliente,
        Phone AS Telefono,  -- No alteramos Telefono
        City AS Ciudad, -- No alteramos Ciudad
        CASE
            WHEN Region IS NULL THEN 'Sin informacion'
            ELSE Region
        END AS Region,
        CASE
            WHEN LEN(PostalCode) < 5 THEN RIGHT('00000' + PostalCode, 5)
            WHEN PostalCode IS NULL THEN 'Sin informacion'
            ELSE PostalCode
        END AS Codigo_Postal,
        UPPER(CASE 
            WHEN Country = 'UK' THEN 'United Kingdom'
            WHEN Country = 'USA' THEN 'United States'
            ELSE Country
        END) AS Pais,
		-- Normalización de la calle
    REPLACE(
        REPLACE(
            REPLACE(
				REPLACE(
					REPLACE(Address, 'C/', 'Calle '),
					'Av.', 'Avenida '),
				'Rda.', 'Ronda '),
			'Plza.', 'Plaza '),
		'Avda.', 'Avenida ') AS Direccion,
        ContactName AS Contacto -- No alteramos Contacto
    FROM Customers
) AS union_cliente;
