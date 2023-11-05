import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import Calendar

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="militar_manage"
)

# Función para abrir la ventana de añadir usuario
def abrir_ventana_agregar():
    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Añadir Usuario")

    nombre_label = tk.Label(ventana_agregar, text="Nombre:")
    nombre_label.grid(row=0, column=0)
    nombre_entry = tk.Entry(ventana_agregar)
    nombre_entry.grid(row=0, column=1)

    apellidos_label = tk.Label(ventana_agregar, text="Apellidos:")
    apellidos_label.grid(row=1, column=0)
    apellidos_entry = tk.Entry(ventana_agregar)
    apellidos_entry.grid(row=1, column=1)

    brigada_label = tk.Label(ventana_agregar, text="Brigada:")
    brigada_label.grid(row=2, column=0)
    brigada_entry = tk.Entry(ventana_agregar)
    brigada_entry.grid(row=2, column=1)

    # Función para añadir usuarios a la base de datos
    def agregar_usuario():
        nombre = nombre_entry.get()
        apellidos = apellidos_entry.get()
        brigada = brigada_entry.get()

        if nombre and apellidos and brigada:
            cursor = db.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, apellidos, brigada) VALUES (%s, %s, %s)",
                           (nombre, apellidos, brigada))
            db.commit()
            cursor.close()

            messagebox.showinfo("Usuario Agregado", "Usuario agregado con éxito.")
            ventana_agregar.destroy()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    agregar_button = tk.Button(ventana_agregar, text="Agregar Usuario", command=agregar_usuario)
    agregar_button.grid(row=4, column=0, columnspan=2)

# Función para editar un usuario
def abrir_ventana_editar():
    def editar_usuario():
        id_usuario = id_entry.get()
        nombre = nombre_entry.get()
        apellidos = apellidos_entry.get()
        brigada = brigada_entry.get()

        if id_usuario and nombre and apellidos and brigada:
            cursor = db.cursor()
            query = "UPDATE usuarios SET nombre = %s, apellidos = %s, brigada = %s WHERE id = %s"
            cursor.execute(query, (nombre, apellidos, brigada, id_usuario))
            db.commit()
            cursor.close()
            messagebox.showinfo("Éxito", "Usuario editado con éxito")
            ventana_editar.destroy()
        else:
            messagebox.showerror("Error", "Debes completar todos los campos")

    ventana_editar = tk.Toplevel(ventana)
    ventana_editar.title("Editar Usuario")

    ttk.Label(ventana_editar, text="ID").grid(row=0, column=0)
    id_entry = ttk.Entry(ventana_editar)
    id_entry.grid(row=0, column=1)

    ttk.Label(ventana_editar, text="Nombre").grid(row=1, column=0)
    nombre_entry = ttk.Entry(ventana_editar)
    nombre_entry.grid(row=1, column=1)

    ttk.Label(ventana_editar, text="Apellidos").grid(row=2, column=0)
    apellidos_entry = ttk.Entry(ventana_editar)
    apellidos_entry.grid(row=2, column=1)

    ttk.Label(ventana_editar, text="Brigada").grid(row=3, column=0)
    brigada_entry = ttk.Entry(ventana_editar)
    brigada_entry.grid(row=3, column=1)

    ttk.Button(ventana_editar, text="Editar Usuario", command=editar_usuario).grid(row=4, column=0, columnspan=2)

# Función para eliminar un usuario
def abrir_ventana_eliminar():
    def eliminar_usuario():
        id_usuario = id_entry.get()

        if id_usuario:
            cursor = db.cursor()
            query = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(query, (id_usuario,))
            db.commit()
            cursor.close()
            messagebox.showinfo("Éxito", "Usuario eliminado con éxito")
            ventana_eliminar.destroy()
        else:
            messagebox.showerror("Error", "Debes ingresar el ID del usuario")

    ventana_eliminar = tk.Toplevel(ventana)
    ventana_eliminar.title("Eliminar Usuario")

    ttk.Label(ventana_eliminar, text="ID").grid(row=0, column=0)
    id_entry = ttk.Entry(ventana_eliminar)
    id_entry.grid(row=0, column=1)

    ttk.Button(ventana_eliminar, text="Eliminar Usuario", command=eliminar_usuario).grid(row=1, column=0, columnspan=2)


# Función para añadir un turno a un usuario ya creado
def abrir_ventana_agregar_turno():
    ventana_agregar_turno = tk.Toplevel(ventana)
    ventana_agregar_turno.title("Agregar Turno")

    fecha_label = tk.Label(ventana_agregar_turno, text="Fecha (DD/MM/YYYY):")
    fecha_label.grid(row=0, column=0)

    fecha_entry = tk.Entry(ventana_agregar_turno)
    fecha_entry.grid(row=0, column=1)

    # Crear un menú desplegable para seleccionar una brigada
    ttk.Label(ventana_agregar_turno, text="Brigada:").grid(row=2, column=0)

    # Consulta a la base de datos para obtener la lista de brigadas
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT brigada FROM usuarios")
    brigadas = cursor.fetchall()
    cursor.close()

    lista_brigadas = [brigada[0] for brigada in brigadas]

    brigadas_combo = ttk.Combobox(ventana_agregar_turno, values=lista_brigadas)
    brigadas_combo.grid(row=2, column=1)

    # Crear un menú desplegable para seleccionar un usuario al que asignar el turno
    ttk.Label(ventana_agregar_turno, text="Usuario:").grid(row=1, column=0)

    usuarios_combo = ttk.Combobox(ventana_agregar_turno, values=[])
    usuarios_combo.grid(row=1, column=1)

    def cargar_usuarios():
        selected_brigada = brigadas_combo.get()
        if selected_brigada:
            cursor = db.cursor()
            # Filtrar usuarios por la brigada seleccionada
            cursor.execute("SELECT nombre, apellidos FROM usuarios WHERE brigada = %s", (selected_brigada,))
            usuarios = cursor.fetchall()
            cursor.close()
            # Combinar nombre y apellido en una sola cadena y convertirlos en una lista
            lista_usuarios = ["{} {}".format(usuario[0], usuario[1]) for usuario in usuarios]
            usuarios_combo["values"] = lista_usuarios
        else:
            usuarios_combo["values"] = []

    brigadas_combo.bind("<<ComboboxSelected>>", lambda event: cargar_usuarios())

    # Crear un menú desplegable para seleccionar el turno (Mañana, Tarde, Noche)
    ttk.Label(ventana_agregar_turno, text="Turno:").grid(row=3, column=0)
    turnos_combo = ttk.Combobox(ventana_agregar_turno, values=["Mañana (M)", "Tarde (T)", "Noche (N)"])
    turnos_combo.grid(row=3, column=1)

    def agregar_turno():
        fecha = fecha_entry.get()
        usuario = usuarios_combo.get()
        brigada = brigadas_combo.get()
        turno = turnos_combo.get()

        if fecha and usuario and brigada and turno:
            # Convertir la fecha al formato "YYYY-MM-DD"
            fecha_parts = fecha.split("/")
            fecha_mysql = "{}-{}-{}".format(fecha_parts[2], fecha_parts[1], fecha_parts[0])

            # Insertar la fecha, usuario, brigada y turno en la tabla Turnos
            cursor = db.cursor()
            cursor.execute("INSERT INTO Turnos (fecha, usuario, brigada, turno) VALUES (%s, %s, %s, %s)",
                           (fecha_mysql, usuario, brigada, turno))
            db.commit()
            cursor.close()

            messagebox.showinfo("Turno Agregado", "Turno agregado con éxito.")
            ventana_agregar_turno.destroy()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    agregar_button = tk.Button(ventana_agregar_turno, text="Agregar Turno", command=agregar_turno)
    agregar_button.grid(row=4, column=0, columnspan=3)


def mostrar_turnos():
    ventana_seleccion = tk.Toplevel(ventana)
    ventana_seleccion.title("Seleccionar Usuario y Brigada")

    # Crear un menú desplegable para seleccionar una brigada
    ttk.Label(ventana_seleccion, text="Brigada:").grid(row=0, column=0)

    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT brigada FROM usuarios")
    brigadas = cursor.fetchall()
    cursor.close()

    lista_brigadas = [brigada[0] for brigada in brigadas]

    brigadas_combo = ttk.Combobox(ventana_seleccion, values=lista_brigadas)
    brigadas_combo.grid(row=0, column=1)

    # Crear un menú desplegable para seleccionar un usuario al que asignar el turno
    ttk.Label(ventana_seleccion, text="Usuario:").grid(row=1, column=0)

    usuarios_combo = ttk.Combobox(ventana_seleccion, values=[])
    usuarios_combo.grid(row=1, column=1)

    def cargar_usuarios():
        selected_brigada = brigadas_combo.get()
        if selected_brigada:
            cursor = db.cursor()
            # Filtrar usuarios por la brigada seleccionada
            cursor.execute("SELECT nombre, apellidos FROM usuarios WHERE brigada = %s", (selected_brigada,))
            usuarios = cursor.fetchall()
            cursor.close()
            # Combinar nombre y apellido en una sola cadena y convertirlos en una lista
            lista_usuarios = ["{} {}".format(usuario[0], usuario[1]) for usuario in usuarios]
            usuarios_combo["values"] = lista_usuarios
        else:
            usuarios_combo["values"] = []

    brigadas_combo.bind("<<ComboboxSelected>>", lambda event: cargar_usuarios())

    def mostrar_turnos_seleccionados():
        selected_usuario = usuarios_combo.get()
        selected_brigada = brigadas_combo.get()

        if selected_usuario and selected_brigada:
            cursor = db.cursor()
            # Obtener los turnos del usuario y brigada seleccionados
            cursor.execute("SELECT fecha, turno, brigada FROM Turnos WHERE usuario = %s AND brigada = %s",
                           (selected_usuario, selected_brigada))
            turnos = cursor.fetchall()
            cursor.close()

            if turnos:
                ventana_turnos = tk.Toplevel(ventana)
                ventana_turnos.title(f"Turnos de {selected_usuario} - {selected_brigada}")

                # Crear una tabla para mostrar los turnos
                tabla_turnos = ttk.Treeview(ventana_turnos, columns=("Fecha", "Turno", "Brigada"), show="headings")
                tabla_turnos.heading("Fecha", text="Fecha")
                tabla_turnos.heading("Turno", text="Turno")
                tabla_turnos.heading("Brigada", text="Brigada")
                tabla_turnos.grid(row=0, column=0)

                for turno in turnos:
                    tabla_turnos.insert("", "end", values=turno)

                # Botón para cerrar la ventana de los turnos
                cerrar_button = tk.Button(ventana_turnos, text="Cerrar", command=ventana_turnos.destroy)
                cerrar_button.grid(row=1, column=0)
            else:
                messagebox.showinfo("Turnos de " + selected_usuario, f"No hay turnos registrados para {selected_usuario} - {selected_brigada}.")
        else:
            messagebox.showerror("Error", "Por favor, selecciona un usuario y una brigada.")

    # Botón para mostrar los turnos
    mostrar_turnos_button = tk.Button(ventana_seleccion, text="Mostrar Turnos", command=mostrar_turnos_seleccionados)
    mostrar_turnos_button.grid(row=2, column=0, columnspan=2)

# Función para abrir la ventana de gestionar turnos
def abrir_ventana_gestionar_turnos():
    gestionar_turnos_frame.grid(row=1, column=0, columnspan=4)
    boton_volver.grid(row=2, column=0, columnspan=4)

# Función para ocultar el conjunto de botones para gestionar turnos
def ocultar_gestionar_turnos():
    gestionar_turnos_frame.grid_forget()
    boton_volver.grid_forget()

# Función para abrir la ventana de lista de usuarios
def mostrar_usuarios():
    ventana_lista_usuarios = tk.Toplevel(ventana)
    ventana_lista_usuarios.title("Lista de Usuarios")

    # Crear ventana secundaria de lista para mostrar los usuarios
    lista_usuarios = ttk.Treeview(ventana_lista_usuarios, columns=("ID", "Nombre", "Apellidos", "Brigada"), show="headings")
    lista_usuarios.heading("ID", text="ID")
    lista_usuarios.heading("Nombre", text="Nombre")
    lista_usuarios.heading("Apellidos", text="Apellidos")
    lista_usuarios.heading("Brigada", text="Brigada")
    lista_usuarios.grid(row=0, column=0)

    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    for usuario in usuarios:
        lista_usuarios.insert("", "end", values=usuario)

    cursor.close()

def resetear_base_de_datos():
    respuesta = messagebox.askquestion("Resetear Base de Datos", "¿Estás seguro de que deseas resetear la base de datos? Esto eliminará todos los datos de usuarios y turnos.")
    if respuesta == "yes":
        cursor = db.cursor()

        # 1. Desactivar restricciones de clave foránea
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        # 2. Eliminar la tabla usuarios
        cursor.execute("DROP TABLE IF EXISTS usuarios")
        cursor.execute("DROP TABLE IF EXISTS turnos")


        # 3. Volver a crear la tabla usuarios
        cursor.execute("""
            CREATE TABLE usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                apellidos VARCHAR(255) NOT NULL,
                brigada VARCHAR(255) NOT NULL
            )
        """)

        # 4. Crear o reemplazar la tabla Turnos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Turnos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                usuario VARCHAR(255) NOT NULL,
                brigada VARCHAR(255) NOT NULL,
                turno VARCHAR(255) NOT NULL
            )
        """)

        # 5. Reactivar restricciones de clave foránea
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")

        db.commit()
        cursor.close()
        messagebox.showinfo("Éxito", "Base de datos reseteada con éxito")

# Función para abrir el conjunto de botones para gestionar usuarios
def abrir_gestionar_usuarios():
    gestionar_usuarios_frame.grid(row=1, column=0, columnspan=4)
    boton_volver.grid(row=2, column=0, columnspan=4)

# Función para ocultar el conjunto de botones para gestionar usuarios
def ocultar_gestionar_usuarios():
    gestionar_usuarios_frame.grid_forget()
    boton_volver.grid_forget()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Usuarios")

# Modificar el tamaño de la ventana (ancho x alto)
ventana.geometry("1920x1080")  # Cambia las dimensiones a las que desees

# Crear un título para el programa
titulo_label = tk.Label(ventana, text="Gestión de Usuarios", font=("Arial", 20))
titulo_label.grid(row=0, column=0, columnspan=4)

# Crear botones en la ventana principal para abrir las ventanas de diálogo
ttk.Button(ventana, text="Gestionar Usuarios", command=abrir_gestionar_usuarios).grid(row=1, column=0, columnspan=4)
# Crear un botón "Turnos" al inicio
ttk.Button(ventana, text="Turnos", command=abrir_ventana_gestionar_turnos).grid(row=2, column=0, columnspan=4)
# Modifica el botón de resetear base de datos
ttk.Button(ventana, text="Resetear Base de Datos", command=resetear_base_de_datos).grid(row=3, column=0, columnspan=4)

# Crear el conjunto de botones para gestionar usuarios y el botón para volver atrás
gestionar_usuarios_frame = ttk.Frame(ventana)
ttk.Button(gestionar_usuarios_frame, text="Añadir Usuario", command=abrir_ventana_agregar).grid(row=0, column=0, padx=10)
ttk.Button(gestionar_usuarios_frame, text="Editar Usuario", command=abrir_ventana_editar).grid(row=0, column=1, padx=10)
ttk.Button(gestionar_usuarios_frame, text="Eliminar Usuario", command=abrir_ventana_eliminar).grid(row=0, column=2, padx=10)
ttk.Button(gestionar_usuarios_frame, text="Ver Usuarios", command=mostrar_usuarios).grid(row=0, column=3, padx=10)
boton_volver = ttk.Button(gestionar_usuarios_frame, text="Volver", command=ocultar_gestionar_usuarios).grid(row=3, column=2, padx=10)


# Crear el conjunto de botones para gestionar turnos
gestionar_turnos_frame = ttk.Frame(ventana)
ttk.Button(gestionar_turnos_frame, text="Añadir Turno", command=abrir_ventana_agregar_turno).grid(row=0, column=0, padx=10)
ttk.Button(gestionar_turnos_frame, text="Mostrar Turnos", command=mostrar_turnos).grid(row=0, column=1, padx=10)
boton_volver = ttk.Button(gestionar_turnos_frame, text="Volver", command=ocultar_gestionar_turnos)

# Iniciar la aplicación
ventana.mainloop()
