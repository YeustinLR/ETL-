--CREAR VISTA vdim_empleado en BD STAGING
CREATE or alter VIEW vdim_empleado AS
SELECT     
	[empleado_id],
	[nombre_empleado],
	[puesto],
	[fecha_contratacion],
	[pais],
	[ciudad],
	[jefatura],
	[salario]
FROM (
	SELECT
		'JD' + CAST(e.CODIGO_EMPLEADO AS VARCHAR(10)) AS empleado_id,
		CASE
			WHEN e.APELLIDO2 is null THEN (e.NOMBRE + ' ' + e.APELLIDO1)
			ELSE (e.NOMBRE + ' ' + e.APELLIDO1 + ' ' + e.APELLIDO2)
		END AS nombre_empleado,
		e.PUESTO AS puesto,       
		 CAST('2020-04-07' AS date ) AS fecha_contratacion,
		CASE 
			WHEN o.PAIS = 'EEUU' THEN 'Estados Unidos'
			ELSE o.PAIS
		END pais,
		o.CIUDAD AS ciudad,
		CASE
			WHEN e.APELLIDO2 is null THEN (e.NOMBRE + ' ' + e.APELLIDO1)
			ELSE (e.NOMBRE + ' ' + e.APELLIDO1 + ' ' + e.APELLIDO2)
		END AS jefatura,
		CASE
			WHEN e.PUESTO = 'Representante Ventas' THEN CAST(650000 AS numeric(25,2))
			WHEN e.PUESTO = 'Secretaria' THEN CAST(400000 AS numeric(25,2))
			WHEN e.PUESTO = 'Subdirector Marketing' THEN CAST(700000 AS numeric(25,2))
			WHEN e.PUESTO = 'Subdirector Ventas' THEN CAST(1000000 AS numeric(25,2))
			WHEN e.PUESTO = 'Director Oficina' THEN CAST(1500000 AS numeric(25,2))
			WHEN e.PUESTO = 'Director General' THEN CAST(3000000 AS numeric(25,2))
		END AS salario
	FROM 
		EMPLEADO_Jardineria e
	JOIN
		OFICINA_Jardineria o ON e.CODIGO_OFICINA = o.CODIGO_OFICINA
	JOIN
		EMPLEADO_Jardineria j ON e.CODIGO_EMPLEADO = j.CODIGO_EMPLEADO
	UNION
	
	SELECT
		'NW' + CAST(e.EmployeeID AS VARCHAR(10)) AS empleado_id,
		(e.FirstName + ' ' + e.LastName) AS nombre_empleado,
		CASE
			WHEN e.Title = 'Sales Representative' THEN 'Representante Ventas' 
			WHEN e.Title = 'Sales Manager' THEN 'Director General'
			WHEN e.Title = 'Inside Sales Coordinator' THEN 'Subdirector Ventas'
			WHEN e.Title = 'Vice President, Sales' THEN 'Director Oficina'
		END AS puesto,
		CASE
            WHEN e.HireDate IS NULL THEN CAST('2020-04-07' AS date )
            ELSE CONVERT(VARCHAR(10), e.HireDate, 120)  -- Convertir la fecha a VARCHAR (formato YYYY-MM-DD)
        END AS [Fecha_Contratacion],
		CASE
			WHEN e.Country = 'USA' THEN 'Estados Unidos'
			WHEN e.Country = 'UK' THEN 'Inglaterra'
		END AS pais,
		e.City AS ciudad,
		(em.FirstName + ' ' + em.LastName) AS jefatura,
		CASE
			WHEN e.Title = 'Sales Representative' THEN CAST(650000 AS numeric(25,2))
			WHEN e.Title = 'Inside Sales Coordinator' THEN CAST(1000000 AS numeric(25,2))
			WHEN e.Title = 'Vice President, Sales' THEN CAST(1500000 AS numeric(25,2))
			WHEN e.Title = 'Sales Manager' THEN CAST(3000000 AS numeric(25,2))
		END AS salario
	FROM
		Employees e
	JOIN
		Employees em ON e.ReportsTo = em.EmployeeID
) AS vdim_empleado;

SELECT * FROM vdim_empleado order by salario
