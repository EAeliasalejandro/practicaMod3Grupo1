import psycopg2
import getpass

# Configuración de conexión a la base de datos en Docker
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credenciales"
DB_USER = "Admin"
DB_PASSWORD = "p4ssw0rdDB"

def conectar_db():
    #Conectar con la base de datos y retornar una conexión
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print("Hubo un error de conexión",e)
        return None

def obtener_datos_usuario(username, password):
    #Consultar la base de datos para obtener los datos d eun usuario apartir de sus credenciales
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = """
        SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
        FROM credenciales c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.username = %s AND c.password_hash = %s;
        """

        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()

        if usuario:
            print("\nDatos del usuario encontrado:")
            print(f"ID: {usuario[0]}")
            print(f"Nombre: {usuario[1]}")
            print(f"Correo: {usuario[2]}")
            print(f"Teléfono: {usuario[3]}")
            print(f"Fecha de Nacimiento: {usuario[4]}")
        else:
            print("\nUsuario o contraseña incorrectos.")


        cursor.close()
        conn.close()
            
    except Exception as e:
        print("Error de consulta a base de datos: ",e)


def insertar_usuario(nombre, correo ,telefono, fecha_nacimiento, username, password):
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()

        #Insertar datos
        cursor.execute(
            """
                INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento) 
                VALUES (%s, %s, %s, %s) RETURNING id_usuario;
            """, (nombre, correo, telefono, fecha_nacimiento)
        )

        # Obtener el ide del usuario recien insertado
        id_usuario = cursor.fetchone()[0]

        #Insertar las credenciales nuevas
        cursor.execute(
            """
                INSERT INTO credenciales (id_usuario, username, password_hash) 
                VALUES (%s, %s, %s);
            """, (id_usuario, username, password)
        )

        #Confirmar los cambios en la base de datos
        conn.commit()
        print("Se insertaron los datos correctamente")

    except Exception as e:
        print("Error al insertar: ", e)
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def actualizar_correo(id_usuario, correoNuevo):
    conn = conectar_db()
    if not conn:
        return
    try:

        cursor = conn.cursor()
        #Modificar un correo apartir del id_usuario
        cursor.execute(
            "UPDATE usuarios SET correo = %s WHERE id_usuario = %s;", (correoNuevo, id_usuario)
        )
        conn.commit()
        print("Correo actualizado correctamente.")

    except Exception as e:
        print("Error al modificar: ", e)
        conn.rollback()    
    
    finally:
        cursor.close()
        conn.close()


def eliminar_usuario(id_usuario):
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        
        #Eliminación de credencial
        cursor.execute("DELETE FROM credenciales WHERE id_credencial = %s;",(id_usuario))

        #Eliminar usuario
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s;",(id_usuario))

        conn.commit()
        print("Usuario eliminado correctamente")

    except Exception as e:
        print("Error al eliminar: ",e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__=="__main__":
    #print("Inicio de sesión en la base de datos")
    #Solicitar credenciales del usuario
    #user = input("Ingrese un usuario: ")
    #Solicitar la contraseña sin que se vea
    #pdw = getpass.getpass("Ingresar contraseña: ")
    #obtener_datos_usuario(user, pdw)

    #Añadir nuevos usuarios
    #print("Insertar nuevos usuarios")
    #nombre = input("Ingresa el nombre del nuevo usuario: ")
    #correo = input("Ingresa el nuevo correo")
    #telefono = input("Ingresa el telefono del nuevo usuario: ")
    #fecha_nacimiento = input("Ingresa la fecha de nacimiento del nuevo usuario: ")
    #username = input("Ingresa el nuevo usuario: ")
    #password = input("Ingresa la contraseña del nuevo usuario: ")
    #insertar_usuario(nombre, correo, telefono, fecha_nacimiento, username, password)

    #Modificar correos
    #id_usuario = input("Ingresa el id del usuario que quieres modificar: ")
    #correoNuevo = input("Ingresa el correo nuevo: ")
    #actualizar_correo(id_usuario,correoNuevo)

    #Elminar usuarios
    id_usuario = input("Ingresa el id del usuario que quieres eliminar: ")
    eliminar_usuario(id_usuario)