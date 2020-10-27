import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


# ·El objeto global 'request' para acceder a los datos de solicitud entrantes que se enviaran a traves de un formulario HTML.
# · La funcion 'url_for' para generar URL's.
# · la funcion flash() para mostrar un mensaje para procesar una solicitud.
# · la funcion 'redirect()' para redirigir al cliente a una funcion diferente.





#aqui estamos creando una funcion que establecera la conexion a la base de datos y la devolvera.
def get_db_connection(): # esta funcion abre una conexion con el archivo de base de datos 'database.db'
    conn = sqlite3.connect('database.db') # y leugo establece establece el atributo 'row_factory' a 'sqlite3
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post
    
                        

# Row para poder tener acceso basado en nombre a las columnas. 
# Esto significa que la conexión con la base de datos devolverá filas que se comportan como diccionarios Python regulares.
#  Por último, la función devuelve el objeto de conexión conn que usará para acceder a la base de datos.





app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

 # en '__name__' tenemos el nombre del modulo de python actual. Se utiliza para indicar a la 
# instancia donde esta ubicada.


 # app.route -> es un decorador que convierte una funcion de python regular en una funcion vista de Flask, que convierte
 # el valor de devolucion de la funcion en una respuesta HTTP que se mostraba mediante un cliente HTTP, como un navegador web.
 
 # Pasa el valor '/' a @app.route() para indicar que esta función responderá a las solicitudes web para la URL /,
 # que es la URL principal.

@app.route('/')
def inicio():
    conn = get_db_connection() #abrimos la conexion con la base de datos usando la funcion 'get_db_connextion'
    posts = conn.execute('SELECT * from posts').fetchall()
    conn.close
    return render_template('index.html', posts=posts)
# A continuación, ejecuta una consulta SQL para seleccionar todas las entradas de la tabla post. 
# Implementa el método fetchall() para recuperar todas las filas del resultado de la consulta. 
# Esto devolverá una lista de las entradas que insertó en la base de datos en el paso anterior.


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

#En esta nueva función de vista, añade una regla de variable <int:post_id> para especificar que la parte tras la 
# barra (/) es un entero positivo (marcado con el conversor int) que necesita para acceder en su función de vista. 
# Flask reconoce esto y pasa su valor al argumento de palabra clave post_id de su función de vista post(). 
# A continuación, utiliza la función get_post() para obtener la entrada de blog asociada con el ID especificado y 
# almacenar el resultado en la variable post, que pasa por una plantilla post.html que pronto creará.


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?,?)',
                    (title, content))
            conn.commit()
            conn.close()
            return  redirect(url_for('inicio'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title: 
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                        'WHERE  id = ? ',
                        (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('inicio'))
    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ? ', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post[id]))
    return redirect(url_for('inicio'))


@app.route('/about')
def acerca_de():
    nombre = 'Autor del Blog : Oswaldo Flores'
    #redes_sociales = ['Twitter','instagram','Gmail']
    redes_sociales = {
        'Twitter': '@oswalgflores',
        'Instagram': '@oswalgflores',
        'Facebook': 'Oswaldo Flores Ruiz',
        'Gmail': 'oswaldogfr2004@gmail.com'
    }
    profesiones = ['Futbolista', 'programador', 'freelancer', 'pianista', 'el mago negro', 'bilingue']
    return render_template('about.html', name=nombre, social_media = redes_sociales, profesiones = profesiones )



 
if __name__ == '__main__':
    app.run(debug=True, port=3000)
