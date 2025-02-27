from flask import Flask, request, make_response, redirect, render_template, url_for, session
import cx_Oracle

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  

# Nueva ruta para manejar la selección del tipo de cotización
@app.route("/set_tipo_cotizacion", methods=['POST'])
def set_tipo_cotizacion():
    tipo = request.form.get('tipo_cotizacion')
   
    session['tipo_cotizacion'] = tipo
    if tipo == 'compra':
        return redirect(url_for('compra'))
    else:
        return redirect(url_for('alquiler'))
        
    
# Conexión a la base de datos
def obtener_productos():
    try:
        connection = cx_Oracle.connect(
            user='PROYECTODB',
            password='PASSWORD',
            dsn='localhost:1521',
            encoding='UTF-8'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT id, nombre, stock, precio FROM ANDAMIOS")
        productos = cursor.fetchall()
        return productos
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()


def obtener_conductores():
    try:
        connection = cx_Oracle.connect(
            user='PROYECTODB',
            password='PASSWORD',
            dsn='localhost:1521',
            encoding='UTF-8'
        )
        cursor = connection.cursor()
        # Obtener conductor y matrícula únicos 
        cursor.execute("""
            SELECT conductor, matricula 
            FROM (
                SELECT conductor, matricula, 
                       ROW_NUMBER() OVER (PARTITION BY conductor ORDER BY id DESC) AS rn 
                FROM ENVIO
            ) 
            WHERE rn = 1
        """)
        conductores = cursor.fetchall()
        return conductores
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()
        

# Ruta para la página de inicio
@app.route("/")
def inicio():
    return render_template('inicio.html')

# Ruta para la página de alquiler
@app.route("/alquiler")
def alquiler():
     n_meses = request.form.get('n_meses')
     session['n_meses'] = n_meses  # Removed the comma that was causing a tuple
     productos = obtener_productos()  # Obtener productos de la base de datos
     conductores = obtener_conductores() 
     return render_template("alquiler.html", productos=productos, conductores=conductores)

# Ruta para la página de cotización
@app.route("/compra")
def compra():
    productos = obtener_productos()  # Obtener productos de la base de datos
    conductores = obtener_conductores()
    return render_template('compra.html', productos=productos, conductores=conductores)


# Ruta para registrar la cotización
@app.route("/registrar_cotizacion", methods=["POST"])
def registrar_cotizacion():
    # Recibir datos del formulario
    nombre_cliente = request.form.get("nombre")
    telefono = request.form.get("telefono")
    correo = request.form.get("correo")
    tipo = request.form.get("tipo")
    producto_seleccionado = request.form.get("producto")
    cantidad = int(request.form.get("cantidad"))
    conductor = request.form.get("conductor")
    destino = request.form.get("destino")
    n_meses = request.form.get("n_meses")
    
    # Obtener el tipo de cotización de la sesión
    tipo_cotizacion = session.get('tipo_cotizacion')
    print(f"Tipo de cotización: {tipo_cotizacion}")  # Debug print
    
    # Variables para almacenar IDs generados
    id_cliente = None
    id_cotizacion = None
    id_envio = None
    id_guia_remision = None

    try:
        connection = cx_Oracle.connect(
            user='PROYECTODB',
            password='PASSWORD',
            dsn='localhost:1521',
            encoding='UTF-8'
        )
        cursor = connection.cursor()

        # Obtener matrícula del conductor
        cursor.execute("""
            SELECT matricula FROM (
                SELECT matricula 
                FROM ENVIO 
                WHERE conductor = :conductor 
                ORDER BY id DESC
            )
            WHERE ROWNUM = 1
        """, {'conductor': conductor})
        
        matricula_result = cursor.fetchone()
        if not matricula_result:
            return "Error: No hay matrícula asociada al conductor", 400
        matricula = matricula_result[0]

        # Obtener el precio del producto seleccionado desde la tabla ANDAMIOS
        cursor.execute("""
            SELECT precio, nombre FROM ANDAMIOS WHERE id = :id_andamios
        """, {'id_andamios': producto_seleccionado})
        producto_result = cursor.fetchone()
        precio_producto = producto_result[0]
        nombre_producto = producto_result[1]

        # Calcular el total (cantidad * precio)
        total = precio_producto * cantidad

        # Aplicar descuento si el cliente es prioritario
        if tipo == "prioritario":
            descuento = cursor.callfunc("aplicar_descuento", cx_Oracle.NUMBER, [total] ) # 10% de descuento para clientes prioritarios
        else:
            descuento = 0.0

        # Calcular el total con descuento
        total_con_descuento = total - descuento 

        # Calcular el IGV (18%) sobre el total con descuento
        igv = cursor.callfunc("aplicar_igv", cx_Oracle.NUMBER, [total_con_descuento] ) 
        
        total_con_descuento=cursor.callfunc("TOTAL_FINAL", cx_Oracle.NUMBER, [total,igv,descuento])

        # Obtener el siguiente id_cliente de la secuencia CLIENTE_SEQ
        cursor.execute("SELECT CLIENTE_SEQ.NEXTVAL FROM dual")
        id_cliente = cursor.fetchone()[0]

        # Registrar el cliente en la tabla CLIENTE
        cursor.execute("""
            INSERT INTO CLIENTE (id, nombre, telefono, gmail, tipo)
            VALUES (:id_cliente, :nombre, :telefono, :correo, :tipo)
        """, {'id_cliente': id_cliente, 'nombre': nombre_cliente, 'telefono': telefono, 'correo': correo, 'tipo': tipo})

        # Obtener el siguiente id_cotizacion de la secuencia COTIZACION_SEQ
        cursor.execute("SELECT COTIZACION_SEQ.NEXTVAL FROM dual")
        id_cotizacion = cursor.fetchone()[0]

        # Obtener el siguiente id_envio de la secuencia ENVIO_SEQ
        cursor.execute("SELECT ENVIO_SEQ.NEXTVAL FROM dual")
        id_envio = cursor.fetchone()[0]

        # Obtener el siguiente id_guia_remision de la secuencia GUIA_REMISION_SEQ
        cursor.execute("SELECT GUIA_REMISION_SEQ.NEXTVAL FROM dual")
        id_guia_remision = cursor.fetchone()[0]
        
        # Registrar envio
        cursor.execute("""
            INSERT INTO ENVIO (id, matricula, transporte, conductor)
            VALUES (:id_envio, :matricula, 'Camion', :conductor)
        """, {'id_envio': id_envio, 'matricula': matricula, 'conductor': conductor})

        # Registrar la cotización en la tabla COTIZACION
        cursor.execute("""
            INSERT INTO COTIZACION (id, id_cliente, id_envio, total, descuento, fecha_generacion, igv)
            VALUES (:id_cotizacion, :id_cliente, :id_envio, :total, :descuento, SYSDATE, :igv)
        """, {'id_cotizacion': id_cotizacion, 'id_cliente': id_cliente, 'id_envio': id_envio, 
              'total': total_con_descuento, 'descuento': descuento, 'igv': igv})

        # Registrar los productos de la cotización en COTIZACION_ANDAMIOS
        cursor.execute("""
            INSERT INTO COTIZACION_ANDAMIOS (id_andamios, id_cotizacion)
            VALUES (:id_andamios, :id_cotizacion)
        """, {'id_andamios': producto_seleccionado, 'id_cotizacion': id_cotizacion})

        # Actualizar el stock del producto en la tabla ANDAMIOS
        cursor.execute("""
            UPDATE ANDAMIOS
            SET stock = stock - :cantidad
            WHERE id = :id_andamios
        """, {'cantidad': cantidad, 'id_andamios': producto_seleccionado})

        # Registrar en la tabla correcta según el tipo de cotización
        print(f"Registrando como {tipo_cotizacion}")  # Debug print
        
        if tipo_cotizacion == 'compra':
            cursor.execute("""
                INSERT INTO VENTA (id_cotizacion)
                VALUES(:id_cotizacion)
            """, {'id_cotizacion': id_cotizacion})
            print(f"Venta registrada con ID: {id_cotizacion}")  # Debug print
        elif tipo_cotizacion == 'alquiler':
            meses_alquiler = int(n_meses) if n_meses else 1
            cursor.execute("""
                INSERT INTO ALQUILER (id_cotizacion, fecha_devolucion, n_meses)
                VALUES(:id_cotizacion, NULL, :meses_alquiler)
            """, {'id_cotizacion': id_cotizacion, 'meses_alquiler': meses_alquiler})
            
            # Solo insertar en ANDAMIOS_ALQUILER si es un alquiler
            cursor.execute("""
                INSERT INTO ANDAMIOS_ALQUILER (id_andamios, id_alquiler)
                VALUES (:id_andamios, :id_alquiler)
            """, {'id_andamios': producto_seleccionado, 'id_alquiler': id_cotizacion})
            
            try:
                cursor.callproc('Insertar_Meses_Alquiler', [id_cotizacion, meses_alquiler])
            except Exception as e:
                print(f"Error en Insertar_Meses_Alquiler: {e}")

        # Registrar la guía de remisión
        cursor.execute("""
            INSERT INTO GUIA_REMISION (id, destino, id_envio, fecha)
            VALUES (:id_guia_remision, :destino, :id_envio, SYSDATE)
        """, {'id_guia_remision': id_guia_remision, 'destino': destino, 'id_envio': id_envio})
        
        # Confirmar los cambios en la base de datos
        connection.commit()

        # Guardar el ID de la cotización en la sesión para recuperarlo en la página de detalle
        session['id_cotizacion'] = id_cotizacion
        session['cantidad'] = cantidad

        # Redirigir a la página de detalle de la cotización
        return redirect(url_for('detalle'))

    except Exception as ex:
        print(f"Error detallado: {ex}")
        import traceback
        traceback.print_exc()
        return f"Error al procesar la cotización: {str(ex)}", 500
    finally:
        connection.close()

    
# Añadir la ruta de búsqueda
@app.route("/buscar_cotizacion", methods=["POST"])
def buscar_cotizacion():
    # Obtener el ID de la cotización del formulario
    id_cotizacion = request.form.get("id_cotizacion")
    
    if not id_cotizacion:
        return "Error: ID de cotización no proporcionado", 400
    
    try:
        connection = cx_Oracle.connect(
            user='PROYECTODB',
            password='PASSWORD',
            dsn='localhost:1521',
            encoding='UTF-8'
        )
        cursor = connection.cursor()
        
        # Verificar si la cotización existe
        cursor.execute("""
            SELECT COUNT(*) FROM COTIZACION WHERE id = :id_cotizacion
        """, {'id_cotizacion': id_cotizacion})
        
        if cursor.fetchone()[0] == 0:
            return "Error: Cotización no encontrada", 404
        
        # Guardar el ID de la cotización en la sesión
        session['id_cotizacion'] = int(id_cotizacion)
        
        # Obtener la cantidad de productos
        cursor.execute("""
            SELECT COUNT(*) FROM COTIZACION_ANDAMIOS WHERE id_cotizacion = :id_cotizacion
        """, {'id_cotizacion': id_cotizacion})
        session['cantidad'] = cursor.fetchone()[0]
        
        # Verificar si es una cotización de tipo compra o alquiler
        cursor.execute("""
            SELECT 'compra' as tipo FROM VENTA WHERE id_cotizacion = :id_cotizacion
            UNION ALL
            SELECT 'alquiler' as tipo FROM ALQUILER WHERE id_cotizacion = :id_cotizacion
        """, {'id_cotizacion': id_cotizacion})
        
        tipo_result = cursor.fetchone()
        if tipo_result:
            session['tipo_cotizacion'] = tipo_result[0]
            print(f"Tipo de cotización encontrado: {tipo_result[0]}")
        else:
            # Verificar cada tabla por separado para diagnóstico
            cursor.execute("SELECT COUNT(*) FROM VENTA WHERE id_cotizacion = :id", {'id': id_cotizacion})
            count_venta = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ALQUILER WHERE id_cotizacion = :id", {'id': id_cotizacion})
            count_alquiler = cursor.fetchone()[0]
            
            print(f"Diagnóstico: Venta={count_venta}, Alquiler={count_alquiler}")
            
            session['tipo_cotizacion'] = 'desconocido'
            print("Tipo de cotización no encontrado, establecido como 'desconocido'")
        
        # Redirigir a la página de detalle
        return redirect(url_for('detalle'))
        
    except Exception as ex:
        print(f"Error detallado: {ex}")
        import traceback
        traceback.print_exc()
        return f"Error al buscar la cotización: {str(ex)}", 500
    finally: 
        connection.close()
# Actualizar la ruta de detalle para mostrar la información de la cotización
@app.route("/detalle")
def detalle():
    # Recuperar el ID de la cotización de la sesión
    id_cotizacion = session.get('id_cotizacion')
    cantidad = session.get('cantidad')
    tipo_cotizacion = session.get('tipo_cotizacion')
    
    if not id_cotizacion:
        return redirect(url_for('inicio'))
    
    try:
        connection = cx_Oracle.connect(
            user='PROYECTODB',
            password='PASSWORD',
            dsn='localhost:1521',
            encoding='UTF-8'
        )
        cursor = connection.cursor()
        
        # Obtener la información de la cotización
        cursor.execute("""
            SELECT c.id, c.total, c.descuento, c.fecha_generacion, c.igv, c.id_cliente, c.id_envio 
            FROM COTIZACION c 
            WHERE c.id = :id_cotizacion
        """, {'id_cotizacion': id_cotizacion})
        
        cotizacion_result = cursor.fetchone()
        if not cotizacion_result:
            return "Error: Cotización no encontrada", 404
            
        cotizacion = {
            'id': cotizacion_result[0],
            'total': cotizacion_result[1],
            'descuento': cotizacion_result[2],
            'fecha_generacion': cotizacion_result[3].strftime('%d/%m/%Y %H:%M'),
            'igv': cotizacion_result[4],
            'id_cliente': cotizacion_result[5],
            'id_envio': cotizacion_result[6]
        }
        
        # Obtener la información del cliente
        cursor.execute("""
            SELECT nombre, telefono, gmail, tipo 
            FROM CLIENTE 
            WHERE id = :id_cliente
        """, {'id_cliente': cotizacion['id_cliente']})
        
        cliente_result = cursor.fetchone()
        cliente = {
            'nombre': cliente_result[0],
            'telefono': cliente_result[1],
            'gmail': cliente_result[2],
            'tipo': cliente_result[3]
        }
        
        # Obtener la información del envío
        cursor.execute("""
            SELECT matricula, conductor 
            FROM ENVIO 
            WHERE id = :id_envio
        """, {'id_envio': cotizacion['id_envio']})
        
        envio_result = cursor.fetchone()
        envio = {
            'matricula': envio_result[0],
            'conductor': envio_result[1]
        }
        
        # Obtener la información de la guía de remisión
        cursor.execute("""
            SELECT destino, fecha 
            FROM GUIA_REMISION 
            WHERE id_envio = :id_envio
        """, {'id_envio': cotizacion['id_envio']})
        
        guia_result = cursor.fetchone()
        guia = {
            'destino': guia_result[0],
            'fecha': guia_result[1].strftime('%d/%m/%Y')
        }
        
        # Obtener la información del producto
        cursor.execute("""
            SELECT a.nombre, a.precio 
            FROM ANDAMIOS a 
            INNER JOIN COTIZACION_ANDAMIOS ca ON a.id = ca.id_andamios 
            WHERE ca.id_cotizacion = :id_cotizacion
        """, {'id_cotizacion': id_cotizacion})
        
        producto_result = cursor.fetchone()
        producto = {
            'nombre': producto_result[0],
            'precio': producto_result[1]
        }
        
        # Verificar el tipo de cotización si no viene en la sesión
        if not tipo_cotizacion or tipo_cotizacion == 'desconocido':
            # Primero verificar si es una venta
            cursor.execute("""
                SELECT COUNT(*) FROM VENTA WHERE id_cotizacion = :id_cotizacion
            """, {'id_cotizacion': id_cotizacion})
            
            if cursor.fetchone()[0] > 0:
                tipo_cotizacion = 'compra'
                session['tipo_cotizacion'] = 'compra'
            else:
                # Verificar si es un alquiler
                cursor.execute("""
                    SELECT COUNT(*) FROM ALQUILER WHERE id_cotizacion = :id_cotizacion
                """, {'id_cotizacion': id_cotizacion})
                
                if cursor.fetchone()[0] > 0:
                    tipo_cotizacion = 'alquiler'
                    session['tipo_cotizacion'] = 'alquiler'
                    
        # Variables para información de alquiler
        fecha_devolucion = None
        meses_alquiler = None
        
        # Obtener fecha de devolución si es un alquiler
        if tipo_cotizacion == 'alquiler':
            try:
                cursor.execute("""
                    SELECT fecha_devolucion, n_meses
                    FROM ALQUILER 
                    WHERE id_cotizacion = :id_cotizacion
                """, {'id_cotizacion': id_cotizacion})
                
                alquiler_result = cursor.fetchone()
                if alquiler_result and alquiler_result[0]:
                    fecha_devolucion = alquiler_result[0].strftime('%d/%m/%Y')
                else:
                    fecha_devolucion = "No establecida"
                    
                meses_alquiler = alquiler_result[1] if alquiler_result and alquiler_result[1] else 0
            except Exception as e:
                print(f"Error al obtener fecha de devolución: {e}")
                fecha_devolucion = "No disponible"
        
        return render_template(
            "detalle.html", 
            cotizacion=cotizacion, 
            cliente=cliente, 
            envio=envio, 
            guia=guia, 
            producto=producto, 
            cantidad=cantidad,
            tipo_cotizacion=tipo_cotizacion,
            fecha_devolucion=fecha_devolucion,
            meses_alquiler=meses_alquiler
        )
        
    except Exception as ex:
        print(f"Error detallado: {ex}")
        import traceback
        traceback.print_exc()
        return f"Error al obtener detalles de la cotización: {str(ex)}", 500
    finally:
        connection.close()

# Redirigir desde el inicio al show_information_address
@app.route("/index")
def index():
    user_ip_information = request.remote_addr
    response = make_response(redirect("show_information_address"))
    response.set_cookie("user_ip_information", user_ip_information)
    return response


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)