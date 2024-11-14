CREATE or alter VIEW vdim_producto AS
SELECT 
    product_id,
    nombre_producto,
    categoria,
    cantidad_por_unidad,
    precio_unitario,
    unidades_en_stock
FROM (
    SELECT 
        CAST(p.CODIGO_PRODUCTO AS VARCHAR(10)) AS product_id,
        p.NOMBRE AS nombre_producto,
        p.GAMA AS categoria,
        'Unico' AS cantidad_por_unidad,  
        p.CANTIDAD_EN_STOCK AS unidades_en_stock,
        p.PRECIO_VENTA AS precio_unitario
	FROM 
        PRODUCTO_Jardineria p

    UNION ALL

    SELECT 
        CAST(p.ProductID AS VARCHAR(10)) AS product_id,
        p.ProductName AS nombre_producto,
        c.CategoryName AS categoria,
        p.QuantityPerUnit AS cantidad_por_unidad,  
        p.UnitPrice AS precio_unitario,
        p.UnitsInStock AS unidades_en_stock
    FROM 
        Products p
    JOIN 
        Categories c ON p.CategoryID = c.CategoryID
    WHERE
        p.Discontinued = 0
) AS P; 