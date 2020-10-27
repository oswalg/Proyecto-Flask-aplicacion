import sqlite3

connection = sqlite3.connect('database.db') #aqui establacemos la conexion con el archivo de la base de datos
 # llamado 'database.db'

with open('schema.sql') as f: # aqui utilice el 'open' para abrir el archivo schema.sql
    connection.executescript(f.read()) # aqui con 'executescript' ejecuta el contenido de la db, que ejecuta 
    #multiples instrucciones de sql a la vez, lo que creara la tabla posts


cur  = connection.cursor()

cur.execute("INSERT INTO posts(title, content) VALUES(?,?)",
    ('First Post', 'Content for the first post')
    )


cur.execute("INSERT INTO posts(title, content) VALUES(?,?)",
    ('Second Post', 'Content for the second post')
    )

connection.commit()
connection.close() #aqui finalmente confirmamos los cambios y se cierra la conexion.

