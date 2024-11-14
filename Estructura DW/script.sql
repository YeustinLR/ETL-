create table dim_cliente(
	cliente_key int identity(1,1) constraint pk_cliente primary key,
	cliente_id nvarchar(5),
	nombre_cliente nvarchar(100),
	pais nvarchar(50),
	ciudad nvarchar(50),
	codigo_postal nvarchar(25),
	telefono nvarchar(20),
	asesor nvarchar(80),
	region nvarchar(100),
	direccion nvarchar(100),
);

---------------------------------------------
---------------------------------------------
create table dim_producto(
	producto_key int identity(1,1) constraint pk_producto primary key,
	product_id varchar(15),
	nombre_producto nvarchar(100),
	categoria varchar(30),
	cantidad_por_unidad int,
	precio_unitario decimal (10,2),
	unidades_en_stock int,
	unidades_en_orden int
);
---------------------------------------------
---------------------------------------------
create table dim_empleado(
	empleado_key int identity(1,1) constraint pk_empleado primary key,
	employee_id varchar(30),
	nombre_empleado nvarchar(100),
	puesto nvarchar(50),
	fecha_contratacion date, 
	pais nvarchar(50),
	ciudad nvarchar(50),
	jefatura varchar (80),
	salario numeric(25,2)
);

---------------------------------------------

---------------------------------------------
create table dim_tiempo(
	fecha_key int identity(1,1) constraint pk_tiempo primary key,
	fecha date,
	annio int,
	mes int,
	dia int,
	cuatrimestre int,
	trimestre int,
	semana int ,
	dia_semana nvarchar(10),
	dia_annio int
);

declare @fecha_inicial date = '2020-01-01';
declare @fecha_final date = '2024-12-31';

while @fecha_inicial <= @fecha_final
begin 
	insert into dim_tiempo(fecha,annio, mes,dia,cuatrimestre, trimestre, semana,dia_semana, dia_annio)
	values(
		@fecha_inicial,
		year(@fecha_inicial),
		month(@fecha_inicial),
		day(@fecha_inicial),
		case
			when month(@fecha_inicial) between 1 and 4 then 1
			when month(@fecha_inicial) between 5 and 8 then 2
			when month(@fecha_inicial) between 9 and 12 then 3
		end,
		case	
			when month(@fecha_inicial) between 1 and 3 then 1
			when month(@fecha_inicial) between 4 and 6 then 2
			when month(@fecha_inicial) between 7 and 9 then 3
			else 4 
		end,
		datepart(week,@fecha_inicial),
		datename(weekday,@fecha_inicial),
		datepart(dayofyear,@fecha_inicial)
		);
		set @fecha_inicial = dateadd(day,1,@fecha_inicial);
end;

---------------------------------------------
---------------------------------------------
create table dim_transportista(
	transportista_key int identity(1,1) constraint pk_transportista primary key,
	transportista_id int,
	nombre_transportista nvarchar(100),
	telefono nvarchar (20)
);
---------------------------------------------
---------------------------------------------
create table fact_ventas(
	venta_idy int identity(1,1) constraint pk_fact_ventas primary key,
	fecha_key int,
	cliente_key int,
	producto_key int,
	empleado_key int,
	transportista_key int,
	cantidad int,
	precio_unitario decimal(12,2),
	total_venta decimal (12,2)	
);

ALTER TABLE FACT_VENTAS ADD CONSTRAINT FK_VENTAS_CLIENTE FOREIGN KEY (cliente_key) REFERENCES dim_cliente(cliente_key);
ALTER TABLE FACT_VENTAS ADD CONSTRAINT FK_VENTAS_EMPLEADO FOREIGN KEY (empleado_key) REFERENCES dim_empleado(empleado_key);
ALTER TABLE FACT_VENTAS ADD CONSTRAINT FK_VENTAS_PRODUCTO FOREIGN KEY (producto_key) REFERENCES dim_producto(producto_key);
ALTER TABLE FACT_VENTAS ADD CONSTRAINT FK_VENTAS_TIEMPO FOREIGN KEY (fecha_key) REFERENCES dim_tiempo(fecha_key);
ALTER TABLE FACT_VENTAS ADD CONSTRAINT FK_VENTAS_TRANSPORTISTA FOREIGN KEY (transportista_key) REFERENCES dim_transportista(transportista_key);
