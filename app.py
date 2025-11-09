# 🏪 SISTEMA WEB PARA BODEGA - EL CEREBRO PRINCIPAL

# Importar las herramientas de Flask
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# Crear la aplicación Flask
app = Flask(__name__)

# FUNCIÓN: Crear la base de datos (como un archivo Excel)
def init_db():
    conn = sqlite3.connect('bodega.db')  # Conectar a la base de datos
    c = conn.cursor()  # Crear un "lápiz" para escribir
    # Crear tabla de productos (como una hoja de Excel)
    c.execute('''CREATE TABLE IF NOT EXISTS productos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT NOT NULL,
                 precio REAL NOT NULL,
                 stock INTEGER NOT NULL)''')
    conn.commit()  # Guardar cambios
    conn.close()   # Cerrar la base de datos

# RUTA 1: Página de Inicio
@app.route('/')
def index():
    return render_template('index.html')  # Mostrar la página principal

# RUTA 2: Página para ver todos los productos
@app.route('/productos')
def ver_productos():
    conn = sqlite3.connect('bodega.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos")  # Leer todos los productos
    productos = c.fetchall()  # Obtener los resultados
    conn.close()
    return render_template('productos.html', productos=productos)

# RUTA 3: Página para agregar productos (acepta formularios)
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':  # Si el usuario envió un formulario
        # Obtener datos del formulario
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        
        # Guardar en la base de datos
        conn = sqlite3.connect('bodega.db')
        c = conn.cursor()
        c.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                 (nombre, precio, stock))
        conn.commit()
        conn.close()
        return redirect(url_for('ver_productos'))  # Redirigir al inventario
    
    return render_template('agregar.html')  # Mostrar el formulario

# RUTA 4: Función para vender productos
@app.route('/vender/<int:producto_id>')
def vender_producto(producto_id):
    conn = sqlite3.connect('bodega.db')
    c = conn.cursor()
    # Restar 1 al stock del producto
    c.execute("UPDATE productos SET stock = stock - 1 WHERE id = ? AND stock > 0", (producto_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('ver_productos'))  # Volver al inventario

# RUTA 5: Página para editar producto (formulario)
@app.route('/editar/<int:producto_id>', methods=['GET'])
def editar_producto_form(producto_id):
    conn = sqlite3.connect('bodega.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    producto = c.fetchone()
    conn.close()
    
    if producto:
        return render_template('editar.html', producto=producto)
    else:
        return "Producto no encontrado", 404

# RUTA 6: Procesar la edición del producto
@app.route('/editar/<int:producto_id>', methods=['POST'])
def editar_producto(producto_id):
    nombre = request.form['nombre']
    precio = request.form['precio']
    stock = request.form['stock']
    
    conn = sqlite3.connect('bodega.db')
    c = conn.cursor()
    c.execute("UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
             (nombre, precio, stock, producto_id))
    conn.commit()
    conn.close()
    
    return redirect(url_for('ver_productos'))





# INICIAR LA APLICACIÓN
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
