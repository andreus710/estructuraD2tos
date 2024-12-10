import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class CarritoCompra(tk.Toplevel):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.title("Carrito de compras")
        self.geometry("400x450")

        # Centrar la ventana
        self.transient(parent)
        self.grab_set()
        self.configure(bg="white")
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        posicion_x = int((ancho_pantalla - 400) / 2)
        posicion_y = int((alto_pantalla - 450) / 2)
        self.geometry(f"400x450+{posicion_x}+{posicion_y}")

        # Icono del carrito de compras
        self.icon_path = "BookManager/Vista/Vendedor/iconos/carrito-de-compras.png"
        self.icon = ImageTk.PhotoImage(Image.open(self.icon_path).resize((24, 24)))
        tk.Label(self, image=self.icon, bg="white").pack(pady=10)

        # Título de la ventana
        tk.Label(self, text="Carrito de compras", font=("Arial", 16), bg="white").pack(pady=10)

        # Crear una tabla para el carrito de compras con scroll
        columns = ("Producto", "Unidades", "Total")
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=5)
        self.tree.pack(side="left", fill="both", expand=True)

        # Barra de scroll vertical
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scroll_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll_y.set)

        # Configurar las columnas
        self.tree.heading("Producto", text="Producto")
        self.tree.column("Producto", anchor="center", width=100)
        self.tree.heading("Unidades", text="Unidades")
        self.tree.column("Unidades", anchor="center", width=100)
        self.tree.heading("Total", text="Total")
        self.tree.column("Total", anchor="center", width=100)

        # Botón para eliminar una fila seleccionada
        eliminar_button = tk.Button(self, text="Eliminar producto", command=self.eliminar_producto, bg="red",
                                    fg="white", font=("Arial", 12))
        eliminar_button.pack(pady=5)

        # Botón para guardar los cambios
        guardar_button = tk.Button(self, text="Guardar cambios", command=self.guardar_cambios, bg="#FFA07A", fg="black",
                                  font=("Arial", 12))
        guardar_button.pack(pady=10)

    def eliminar_producto(self):
        selected_item = self.tree.selection()  # Obtener la fila seleccionada
        if selected_item:
            self.tree.delete(selected_item)  # Eliminar la fila seleccionada

    def guardar_cambios(self):
        # Actualizar la lista del carrito en la ventana principal
        self.parent.carrito_compras = []
        for item in self.tree.get_children(): # Recorrer todas las filas para obtener los valores
            values = self.tree.item(item, 'values')
            producto, unidades, total = values
            self.parent.carrito_compras.append((producto, int(unidades), total))
        self.destroy()  # Eliminar la fila seleccionada