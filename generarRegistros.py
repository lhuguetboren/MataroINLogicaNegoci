import random
import datetime

sql = "INSERT INTO cliente (id, nombre, apellido, telefono, email, comentarios, fecha_nacimiento, direccion, id_pais, fecha_entrada, fecha_salida, precio, f_crea, f_elim, f_modif) VALUES\n"

for i in range(1, 101):
    nombre = f"Nombre{i}"
    apellido = f"Apellido{i}"
    telefono = f"{random.randint(100000000, 999999999)}"
    email = f"email{i}@example.com"
    comentarios = "Comentario " + str(i)
    fecha_nacimiento = str(datetime.date(1980 + i % 40, 1, 1))
    direccion = f"Calle {i}"
    id_alojamiento = random.randint(50, 356)
    id_pais = random.randint(1, 51)
    fecha_entrada = '2023-01-01'
    fecha_salida = '2024-'+str(random.randint(1,12))+"-"+str(random.randint(1,30))
    precio = random.uniform(100, 300)
    f_crea = '2023-01-01'
    f_elim = 'NULL'
    f_modif = '2023-01-01'

    sql += f"    ({i}, '{nombre}', '{apellido}', '{telefono}', '{email}', '{comentarios}', '{fecha_nacimiento}', '{direccion}', {id_pais}, '{fecha_entrada}', '{fecha_salida}', {precio:.2f}, '{f_crea}', {f_elim}, '{f_modif}'),\n"

sql = sql.rstrip(',\n') + ';'

print(sql)
