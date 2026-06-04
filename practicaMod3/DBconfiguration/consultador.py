import psycopg2

#1.- Conexión a la base de datos
conexion = psycopg2.connect(
    host="localhost",
    port="5432",
    database="credenciales",
    user="Admin",
    password="p4ssw0rdDB"
)

#2.- Crear cursor
cursor = conexion.cursor()

#3.- Ejecutar una consulta
cursor.execute("SELECT * FROM usuarios;")
                    #fetchone() = una fila
registros = cursor.fetchall() #Para obtener todos los datos devueltos en una lista de tuplas

#4.- Mostrar los resultados
for fila in registros:
    print(fila)
#print(registros)    

#5.- Cerrar la conexión
cursor.close()
conexion.close()