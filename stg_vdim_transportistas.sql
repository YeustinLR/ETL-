CREATE  VIEW vdim_transportista AS
SELECT 
    ShipperID AS transportista_id,
    CompanyName AS nombre_transportista,
    Phone AS telefono
FROM Shippers;
select* from vdim_transportista