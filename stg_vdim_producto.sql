CREATE or alter VIEW vdim_producto AS
SELECT 
    product_id,
    nombre_producto,
    categoria,
    cantidad_por_unidad,
    precio_unitario,
    unidades_en_stock,
    unidades_en_orden
FROM (
    SELECT 
        CAST(p.CODIGO_PRODUCTO AS VARCHAR(10)) AS product_id,
        p.NOMBRE AS nombre_producto,
        p.GAMA AS categoria,
        'Unico' AS cantidad_por_unidad,  
        p.CANTIDAD_EN_STOCK AS unidades_en_stock,
        p.PRECIO_VENTA AS precio_unitario,
        dp.CANTIDAD AS unidades_en_orden
    FROM 
        PRODUCTO_Jardineria p
    JOIN 
        DETALLE_PEDIDO_Jardineria dp ON p.CODIGO_PRODUCTO = dp.CODIGO_PRODUCTO
    JOIN 
        PEDIDO_Jardineria ped ON dp.CODIGO_PEDIDO = ped.CODIGO_PEDIDO

    UNION
    SELECT 
        CAST(p.ProductID AS VARCHAR(10)) AS product_id,
        p.ProductName AS nombre_producto,
        c.CategoryName AS categoria,
        p.QuantityPerUnit AS cantidad_por_unidad,  
        p.UnitPrice AS precio_unitario,
        p.UnitsInStock AS unidades_en_stock,
        p.UnitsOnOrder AS unidades_en_orden
    FROM 
        Products p
    JOIN 
        Categories c ON p.CategoryID = c.CategoryID
    JOIN 
        Suppliers s ON p.SupplierID = s.SupplierID
    WHERE
        p.Discontinued = 0
) AS P;  

SELECT * FROM vdim_producto