--CREAR VISTA vdim_fact_ventas en BD STAGING
CREATE or alter VIEW vdim_fact_ventas AS
SELECT     
	fecha_key,
	cliente_key,
	producto_key,
	empleado_key,
	transportista_key,
	cantidad,
	precio_unitario,
	total,
	descuento
FROM (
SELECT 
    (SELECT fecha_key 
     FROM dw.dbo.dim_tiempo 
     WHERE fecha = p.fecha_pedido) AS fecha_key,
    
    (SELECT cliente_key 
     FROM dw.dbo.dim_cliente 
     WHERE cliente_id = CAST(p.codigo_cliente AS nvarchar(50))) AS cliente_key,

    dp_prod.producto_key,
    
        dp_emp.empleado_key,

    1 AS transportista_key,
    dp.cantidad AS cantidad,
    dp.precio_unidad AS precio_unitario,
    dp.cantidad * dp.precio_unidad AS total,
    0 AS descuento
FROM stg.dbo.PEDIDO_Jardineria p
INNER JOIN stg.dbo.DETALLE_PEDIDO_Jardineria dp 
    ON p.codigo_pedido = dp.codigo_pedido
LEFT JOIN stg.dbo.CLIENTE_Jardineria cl 
    ON cl.codigo_cliente = p.codigo_cliente
LEFT JOIN dw.dbo.dim_producto dp_prod 
    ON dp_prod.product_id = CAST(dp.codigo_producto AS nvarchar(50)) -- 
LEFT JOIN dw.dbo.dim_empleado dp_emp 
    ON CAST(SUBSTRING(dp_emp.employee_id, 3, LEN(dp_emp.employee_id) - 2) AS INT) = CAST(cl.codigo_empleado_rep_ventas AS INT)
    AND SUBSTRING(dp_emp.employee_id, 1, 1) = 'J' -- Asumiendo que es 'J' ;

UNION ALL

SELECT 
	 (SELECT fecha_key 
		FROM dw.dbo.dim_tiempo dt 
     WHERE dt.fecha = CAST(CASE 
                             WHEN YEAR(o.OrderDate) = 1996 THEN DATEADD(YEAR, 25, o.OrderDate)  -- Suma 25 años si el año es 1996
							 WHEN YEAR(o.OrderDate) = 1997 THEN DATEADD(YEAR, 25, o.OrderDate)
							 WHEN YEAR(o.OrderDate) = 1998 THEN DATEADD(YEAR, 25, o.OrderDate)
							 WHEN YEAR(o.OrderDate) = 1999 THEN DATEADD(YEAR, 25, o.OrderDate)
								ELSE o.OrderDate  -- Si no es 1996, usar la fecha original
                             END AS date)
     ) AS fecha_key,
    dc.cliente_key AS cliente_key,                  
    dp.producto_key AS producto_key,                
    de.empleado_key AS empleado_key,               
	(SELECT transportista_key FROM dw.dbo.dim_transportista WHERE transportista_key = o.shipvia) AS transportista_key, -- Clave del TRANSPORTISTA en la tabla dim_TRANSPORTISTA
    od.Quantity AS cantidad,                     -- Cantidad de producto
    od.UnitPrice AS precio_unitario,                    -- Precio por unidad
    od.quantity * od.unitprice * (1 - od.discount) AS Total, -- Total (Cantidad * Precio por unidad)
	od.Discount AS descuento
FROM 
    stg.dbo.Orders o
JOIN 
    dw.dbo.dim_empleado de 
        ON o.EmployeeID = CAST(RIGHT(de.employee_id, LEN(de.employee_id) - 2) AS INT)  -- Extraemos el número de employee_id
        AND LEFT(de.employee_id, 2) = 'NW' -- Filtramos solo los employee_id que inician con 'NW'
JOIN 
    stg.dbo.Order_Details od ON o.OrderID = od.OrderID  -- Relacionamos órdenes con los detalles
JOIN 
    stg.dbo.Products p ON od.ProductID = p.ProductID  -- Relacionamos productos con los detalles de la orden
JOIN 
    dw.dbo.dim_producto dp 
        ON TRY_CAST(dp.product_id AS INT) = p.ProductID  -- Relacionamos con la tabla dim_producto
JOIN 
    dw.dbo.dim_cliente dc 
        ON o.CustomerID = dc.cliente_id  -- Relacionamos Orders con dim_cliente por CustomerID

)AS vdim_fact_ventas;

select * from vdim_fact_ventas