
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
	[Cliente_ID]
		,[Nombre_Cliente]
		,NULL AS[Telefono]
		,NULL AS[Direccion]
		,NULL AS[Ciudad]
		,[Region]
		,[Codigo_Postal]
		,[Pais]
		,NULL AS [Contacto]
FROM (
    --(pais de la tabla cliente) Normalizar país
    SELECT 
        CAST(CODIGO_CLIENTE AS VARCHAR(10)) AS [Cliente_ID],
        NOMBRE_CLIENTE,
        UPPER(CASE 
            WHEN pais = 'UK' THEN 'United Kingdom'
            WHEN pais = 'USA' THEN 'United States'
            ELSE pais
		END) AS pais,
			--Normalizar codigo postal
			CASE
			WHEN LEN(codigo_postal) < 5 THEN RIGHT('00000' + codigo_postal, 5)
			ELSE codigo_postal
		END AS codigo_postal,
			CASE
			WHEN Region is null THEN 'Sin informacion'
			ELSE Region
		END AS Region,
		-- Normalización de la calles
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(LINEA_DIRECCION1, 'C/', 'Calle '),
                'Av.', 'Avenida '),
            'Rda.', 'Ronda '),
        'Plza.', 'Plaza ') AS Direccion
    FROM CLIENTE_Jardineria


    UNION

    --(country de la tabla Customers) Normalizar país
    SELECT 
        CUSTOMERID,
        CompanyName AS nombre_cliente,
        UPPER(CASE 
            WHEN country = 'UK' THEN 'United Kingdom'
            WHEN country = 'USA' THEN 'United States'
            ELSE country
        END) AS pais,
			CASE
			WHEN Region is null THEN 'Sin informacion'
			ELSE Region
		END AS Region,
		--Normalizar codigo postal
			CASE
			WHEN LEN(PostalCode) < 5 THEN RIGHT('00000' + PostalCode, 5)
			WHEN PostalCode is null THEN 'Sin informacion'
			ELSE PostalCode
		END AS codigo_postal,
		-- Normalización de la calle
    REPLACE(
        REPLACE(
            REPLACE(
				REPLACE(
					REPLACE(Address, 'C/', 'Calle '),
					'Av.', 'Avenida '),
				'Rda.', 'Ronda '),
			'Plza.', 'Plaza '),
		'Avda.', 'Avenida ') AS Direccion

    FROM CUSTOMERS
) AS union_cliente