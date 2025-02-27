CREATE TABLE CLIENTE(
    id NUMBER,
    telefono NUMBER,
    nombre VARCHAR(50),
    gmail VARCHAR(50),
    tipo VARCHAR(50),
    PRIMARY KEY(id)
);

CREATE TABLE COTIZACION (
    id NUMBER,
    id_cliente NUMBER,
    id_envio NUMBER,
    total NUMBER(10,2),
    descuento NUMBER(10,2),
    fecha_generacion DATE,
    igv NUMBER(10,2),
    PRIMARY KEY (id),
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id),
    FOREIGN KEY (id_envio) REFERENCES ENVIO(id)
);

CREATE TABLE COTIZACION_ANDAMIOS(
    id_andamios NUMBER,
    id_cotizacion NUMBER,
    FOREIGN KEY (id_andamios) REFERENCES ANDAMIOS(id),
    FOREIGN KEY (id_cotizacion) REFERENCES COTIZACION(id)
);

CREATE TABLE ANDAMIOS(
    id NUMBER,
    nombre VARCHAR(50),
    descripcion VARCHAR(50),
    precio NUMBER(10,2),
    stock NUMBER,
    PRIMARY KEY(id)
);

CREATE TABLE ANDAMIOS_ALQUILER(
    id_andamios NUMBER,
    id_alquiler NUMBER,
    FOREIGN KEY(id_alquiler) REFERENCES ALQUILER(id_cotizacion),
    FOREIGN KEY(id_andamios) REFERENCES ANDAMIOS(id)
);



-- Herencia: COTIZACION -> Venta y Alquiler
CREATE TABLE Venta (
    id_cotizacion NUMBER PRIMARY KEY,
    FOREIGN KEY (id_cotizacion) REFERENCES COTIZACION(id)
);

CREATE TABLE Alquiler (
    id_cotizacion NUMBER PRIMARY KEY,
    fecha_devolucion DATE, -- Atributo específico de alquiler
    n_meses number,
    FOREIGN KEY (id_cotizacion) REFERENCES COTIZACION(id)
);

CREATE TABLE ENVIO(
    id NUMBER,
    id_guia NUMBER,
    matricula NUMBER,
    transporte VARCHAR(50),
    conductor VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE GUIA_REMISION(
    id NUMBER,
    destino VARCHAR(50),
    id_envio NUMBER,
    fecha DATE,
    PRIMARY KEY (id),
    FOREIGN KEY (id_envio) REFERENCES ENVIO(id)
);

select * from andamios;
select * from cliente;
select * from envio;
select * from guia_remision;
select * from andamios_alquiler;
INSERT INTO ANDAMIOS  VALUES (1, 'Ringscaff Pieza de arranque galvanizada', 'Base collar para andamiaje', 12.50, 100);
INSERT INTO ANDAMIOS  VALUES(2, 'Ringscaff Vertical con espiga longitud 2,00 metros', 'Vertical de andamiaje con espiga atornillada', 25.30, 200);
INSERT INTO ANDAMIOS  VALUES(3, 'Ringscaff Plataforma de acero', 'Plataforma metálica para apoyo en tubo', 35.40, 50);
INSERT INTO ANDAMIOS  VALUES(4, 'Ringscaff Rodapié 1,09 m3 acero', 'Rodapié de acero para andamiaje', 8.90, 150);
INSERT INTO ANDAMIOS  VALUES(5, 'Ringscaff Celosía H=0,45 m; L=5,14 m; galvanizada', 'Celosía de acero galvanizado', 75.60, 30);

INSERT INTO CLIENTE VALUES(1,976328654,'EdificacionesSAC','contacto@edificaciones.com','no prioritario');
INSERT INTO CLIENTE VALUES(2,954251336,'Constructora De las Casas','info@constructoralascasas.com','prioritario');
INSERT INTO CLIENTE VALUES(3,924765123,'PeruPetroleo','contacto@perupetroleo.com','no prioritario');
INSERT INTO CLIENTE VALUES(4,967832475,'ABCConsultorias','contacto@abc.com','prioritario');
INSERT INTO CLIENTE VALUES(5,923567842,'EcoIndustrias','contacto@ecoindustrias.com','no prioritario');


INSERT INTO ENVIO (id, id_guia, matricula, transporte, conductor) VALUES (1, 1001, 987654, 'Camión', 'Juan Pérez');
INSERT INTO ENVIO (id, id_guia, matricula, transporte, conductor) VALUES (2, 1002, 987655, 'Camión', 'Carlos Gómez');
INSERT INTO ENVIO (id, id_guia, matricula, transporte, conductor) VALUES (3, 1003, 987656, 'Camión', 'Ana Rodríguez');
INSERT INTO ENVIO (id, id_guia, matricula, transporte, conductor) VALUES (4, 1004, 987657, 'Camión', 'Pedro Fernández');
INSERT INTO ENVIO (id, id_guia, matricula, transporte, conductor) VALUES (5, 1005, 987658, 'Camión', 'María González');




INSERT INTO COTIZACION (id, id_cliente, id_envio, total, descuento, fecha_generacion, igv )VALUES (1, 1, 1, 2000.00, 100.00, TO_DATE('2025-02-10', 'YYYY-MM-DD'), 360.00);
INSERT INTO COTIZACION (id, id_cliente, id_envio, total, descuento, fecha_generacion, igv) VALUES (2, 2, 2, 5000.00, 200.00, TO_DATE('2025-02-12', 'YYYY-MM-DD'), 900.00);
INSERT INTO COTIZACION (id, id_cliente, id_envio, total, descuento, fecha_generacion, igv)VALUES (3, 3, 3, 800.00, 50.00, TO_DATE('2025-02-14', 'YYYY-MM-DD'), 144.00);
INSERT INTO COTIZACION (id, id_cliente, id_envio, total, descuento, fecha_generacion, igv)VALUES (4, 4, 4, 3000.00, 150.00, TO_DATE('2025-02-15', 'YYYY-MM-DD'), 540.00);
INSERT INTO COTIZACION (id, id_cliente, id_envio, total, descuento, fecha_generacion, igv)VALUES (5, 5, 5, 4500.00, 250.00, TO_DATE('2025-02-17', 'YYYY-MM-DD'), 810.00);

INSERT INTO COTIZACION_ANDAMIOS (id_andamios, id_cotizacion) VALUES (1, 1);
INSERT INTO COTIZACION_ANDAMIOS (id_andamios, id_cotizacion) VALUES (2, 1);
INSERT INTO COTIZACION_ANDAMIOS (id_andamios, id_cotizacion) VALUES (3, 2);
INSERT INTO COTIZACION_ANDAMIOS (id_andamios, id_cotizacion) VALUES (4, 3);
INSERT INTO COTIZACION_ANDAMIOS (id_andamios, id_cotizacion) VALUES (5, 4);


INSERT INTO ANDAMIOS_DEVOLUCION (id_andamios, id_devolucion) VALUES (1, 1);
INSERT INTO ANDAMIOS_DEVOLUCION (id_andamios, id_devolucion) VALUES (2, 2);
INSERT INTO ANDAMIOS_DEVOLUCION (id_andamios, id_devolucion) VALUES (3, 3);
INSERT INTO ANDAMIOS_DEVOLUCION (id_andamios, id_devolucion) VALUES (4, 4);
INSERT INTO ANDAMIOS_DEVOLUCION (id_andamios, id_devolucion) VALUES (5, 5);


INSERT INTO Venta (id_cotizacion) VALUES (1);
INSERT INTO Venta (id_cotizacion) VALUES (2);
INSERT INTO Venta (id_cotizacion) VALUES (3);
INSERT INTO Venta (id_cotizacion) VALUES (4);
INSERT INTO Venta (id_cotizacion) VALUES (5);


INSERT INTO Alquiler (id_cotizacion, fecha_devolucion) VALUES (1, TO_DATE('2025-03-01', 'YYYY-MM-DD'));
INSERT INTO Alquiler (id_cotizacion, fecha_devolucion) VALUES (2, TO_DATE('2025-03-05', 'YYYY-MM-DD'));
INSERT INTO Alquiler (id_cotizacion, fecha_devolucion) VALUES (3, TO_DATE('2025-03-10', 'YYYY-MM-DD'));
INSERT INTO Alquiler (id_cotizacion, fecha_devolucion) VALUES (4, TO_DATE('2025-03-15', 'YYYY-MM-DD'));
INSERT INTO Alquiler (id_cotizacion, fecha_devolucion) VALUES (5, TO_DATE('2025-03-20', 'YYYY-MM-DD'));


INSERT INTO GUIA_REMISION (id, destino, id_envio, fecha) VALUES (1, 'Lima', 1, TO_DATE('2025-02-10', 'YYYY-MM-DD'));
INSERT INTO GUIA_REMISION (id, destino, id_envio, fecha) VALUES (2, 'Arequipa', 2, TO_DATE('2025-02-12', 'YYYY-MM-DD'));
INSERT INTO GUIA_REMISION (id, destino, id_envio, fecha) VALUES (3, 'Trujillo', 3, TO_DATE('2025-02-14', 'YYYY-MM-DD'));
INSERT INTO GUIA_REMISION (id, destino, id_envio, fecha) VALUES (4, 'Cusco', 4, TO_DATE('2025-02-15', 'YYYY-MM-DD'));
INSERT INTO GUIA_REMISION (id, destino, id_envio, fecha) VALUES (5, 'Piura', 5, TO_DATE('2025-02-17', 'YYYY-MM-DD'));



--Sequence

CREATE SEQUENCE CLIENTE_SEQ
  START WITH 40
  INCREMENT BY 1
  NOCACHE;

CREATE SEQUENCE COTIZACION_SEQ
  START WITH 40
  INCREMENT BY 1
  NOCACHE;

CREATE SEQUENCE GUIA_REMISION_SEQ
  START WITH 40
  INCREMENT BY 1
  NOCACHE;

CREATE SEQUENCE ENVIO_SEQ
  START WITH 40
  INCREMENT BY 1
  NOCACHE;


commit;





--QUEDA BACK
create or replace Procedure prioridad(n cotizacion.id%type)as
monto number;
promedio number;
begin
select total into monto from Cotizacion where n = id ;
select avg(total) into promedio from Cotizacion;

if monto>=promedio then
update Cliente set tipo='prioritario' where id=n;
DBMS_OUTPUT.PUT_LINE('El cliente con el id '||n||' es prioritario');
else
update Cliente set tipo='no prioritario' where id=n;
DBMS_OUTPUT.PUT_LINE('El cliente con el id '||n||' no es prioritario');

end if;
end; 
/
--QUEDA BACK
set serveroutput on;
CREATE OR REPLACE Procedure actualizar_cliente(n CLIENTE.ID%TYPE, telf cliente.telefono%type,ac_nombre cliente.nombre%type, ac_gmail cliente.gmail%type,ac_tipo cliente.tipo%type)as 
verificar number;
begin 
if verificar = 0 then
SELECT count(*) into verificar from CLIENTE where id = n;
DBMS_OUTPUT.PUT_LINE('Error: No existe un cliente con el ID ' || n);
else
update cliente set telefono=telf, nombre=ac_nombre,gmail=ac_gmail, tipo=ac_tipo where id = n;
commit;
DBMS_OUTPUT.PUT_LINE('Se realizaron los cambios al CLIENTE con id: ' || n);
end if;
end;
select * from cliente;
execute actualizar_cliente(17,123456789,'ethan conde','mocito@gmail.com','No prioritario')



--QUEDA PYTHON
CREATE OR REPLACE PROCEDURE Insertar_Meses_Alquiler(
    p_id_cotizacion IN NUMBER,
    p_meses IN NUMBER
) AS
BEGIN
    UPDATE ALQUILER 
    SET fecha_devolucion = ADD_MONTHS(SYSDATE, p_meses)
    WHERE id_cotizacion = p_id_cotizacion;
    COMMIT;
END;
/
select * from alquiler;

--QUEDA PYTHON
create or replace function TOTAL_FINAL(
TOTAL number,
impuesto number,
descuento number 
)return number as
finales number;
begin
finales := total + impuesto -descuento;
return finales;
end TOTAL_FINAL ;

SELECT TOTAL_FINAL(100, 18, 5) AS RESULTADO FROM DUAL;
SELECT TOTAL_FINAL(100, 18.25, 5.50) AS RESULTADO FROM DUAL;

--QUEDA PYTHON
CREATE OR REPLACE FUNCTION aplicar_descuento(total number)
return number as
descuento number;
begin 
descuento := total*0.1;
return descuento;
end;
SELECT aplicar_descuento(100) AS RESULTADO FROM DUAL;
--QUEDA PYTHON
CREATE OR REPLACE FUNCTION aplicar_igv(total_descuento number)
return number as
impuesto number;
begin 
impuesto := total_descuento*0.18;
return impuesto;
end;
SELECT aplicar_igv(100) AS RESULTADO FROM DUAL;
set serveroutput on;



--trigger
CREATE OR REPLACE TRIGGER reabastecer_stock_andamios
AFTER UPDATE ON ANDAMIOS
DECLARE
    CURSOR c_andamios IS
        SELECT id FROM ANDAMIOS WHERE stock = 0;
BEGIN
    FOR r IN c_andamios LOOP
        UPDATE ANDAMIOS
        SET stock = stock + 20
        WHERE id = r.id;
        
        DBMS_OUTPUT.PUT_LINE('El stock del andamio con ID ' || r.id || ' llegó a 0 y se ha reabastecido con 20 unidades.');
    END LOOP;
END;
/

ALTER TRIGGER reabastecer_stock_andamios DISABLE;





select * from andamios
select * from cliente
select * from alquiler

alter table alquiler add n_meses number

CREATE OR REPLACE PROCEDURE insert_n_meses(n_meses IN NUMBER) 
IS
    CURSOR alquileres IS
        SELECT id, fecha_devolucion FROM alquiler;
    
    v_n_meses NUMBER;
BEGIN
    FOR alquiler IN alquileres LOOP
        v_n_meses := MONTHS_BETWEEN(SYSDATE, alquiler.fecha_devolucion);

        INSERT INTO ALQUILER (id, fecha_devolucion, n_meses) 
        VALUES (alquiler.id, alquiler.fecha_devolucion, v_n_meses);
    END LOOP;
END;
/



SELECT sequence_name FROM user_sequences;
commit













      
