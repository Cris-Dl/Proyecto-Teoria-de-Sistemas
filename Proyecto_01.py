import tkinter as tk
from tkinter import messagebox


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("GEOS - Herramientas y Equipos")
        self.root.geometry("630x700")
        self.root.configure(bg="#FFC300")
        self.root.resizable(False, False)

        # --- DEFINICIÓN DE COLORES ---
        self.COLOR_FONDO = "#FFC300"  # Amarillo mostaza
        self.COLOR_AZUL = "#0066CC"  # Azul fuerte
        self.COLOR_BLANCO = "#FFFFFF"
        self.COLOR_INPUT = "#FFD54F"  # Amarillo más claro para inputs
        self.COLOR_BORDE = "#0055A5"

        self.centrar_ventana(630, 700)

        # --- LOGO SUPERIOR ---
        self.imagen = tk.PhotoImage(file="logo_geos.png")
        self.label_logo = tk.Label(self.root, image=self.imagen, bg=self.COLOR_FONDO)
        self.label_logo.pack(pady=(40, 30))

        # --- CONTENEDOR PRINCIPAL (Cuadro con borde azul redondeado) ---
        self.frame_login = tk.Frame(self.root, bg=self.COLOR_FONDO, width=450, height=380)
        self.frame_login.pack(pady=20)
        self.frame_login.pack_propagate(False)

        # Canvas para crear bordes redondeados
        self.canvas_border = tk.Canvas(self.frame_login, width=450, height=380,
                                       bg=self.COLOR_FONDO, highlightthickness=0)
        self.canvas_border.pack()

        # Rectángulo con bordes redondeados
        self.canvas_border.create_rounded_rectangle(10, 10, 440, 370,
                                                    radius=20,
                                                    outline=self.COLOR_AZUL,
                                                    width=4,
                                                    fill=self.COLOR_FONDO)

        # --- FRAME PARA INPUTS (Dentro del canvas) ---
        self.frame_inputs = tk.Frame(self.frame_login, bg=self.COLOR_FONDO)
        self.frame_inputs.place(x=50, y=50, width=350, height=280)

        # --- INPUT USUARIO ---
        self.frame_user = tk.Frame(self.frame_inputs, bg=self.COLOR_INPUT,
                                   highlightbackground=self.COLOR_AZUL,
                                   highlightthickness=2)
        self.frame_user.pack(pady=(20, 0))

        # Icono Usuario
        tk.Label(self.frame_user, text="👤", font=("Arial", 16),
                 bg=self.COLOR_INPUT, fg=self.COLOR_AZUL).pack(side="left", padx=(10, 5))

        # Entry Usuario
        self.entry_user = tk.Entry(self.frame_user, font=("Arial", 12),
                                   bg=self.COLOR_INPUT, fg="#333333",
                                   relief="flat", width=25)
        self.entry_user.pack(side="left", padx=(5, 10), pady=12)
        self.entry_user.insert(0, "Usuario")
        self.entry_user.bind("<FocusIn>", self.clear_placeholder_user)
        self.entry_user.bind("<FocusOut>", self.restore_placeholder_user)

        # --- INPUT CONTRASEÑA ---
        self.frame_pass = tk.Frame(self.frame_inputs, bg=self.COLOR_INPUT,
                                   highlightbackground=self.COLOR_AZUL,
                                   highlightthickness=2)
        self.frame_pass.pack(pady=(20, 0))

        # Icono Candado
        tk.Label(self.frame_pass, text="🔒", font=("Arial", 16),
                 bg=self.COLOR_INPUT, fg=self.COLOR_AZUL).pack(side="left", padx=(10, 5))

        # Entry Contraseña
        self.entry_password = tk.Entry(self.frame_pass, font=("Arial", 12),
                                       bg=self.COLOR_INPUT, fg="#333333",
                                       relief="flat", width=25)
        self.entry_password.pack(side="left", padx=(5, 10), pady=12)
        self.entry_password.insert(0, "Contraseña")
        self.entry_password.bind("<FocusIn>", self.clear_placeholder_pass)
        self.entry_password.bind("<FocusOut>", self.restore_placeholder_pass)
        self.password_hidden = False

        # --- BOTÓN INICIAR SESIÓN ---
        self.boton_login = tk.Button(self.frame_inputs, text="INICIAR SESIÓN",
                                     bg=self.COLOR_AZUL, fg="white",
                                     font=("Arial", 12, "bold"),
                                     relief="flat", cursor="hand2",
                                     width=30, height=2,
                                     command=self.login)
        self.boton_login.pack(pady=(30, 0))

    def centrar_ventana(self, ancho, alto):
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def clear_placeholder_user(self, event):
        if self.entry_user.get() == "Usuario":
            self.entry_user.delete(0, 'end')
            self.entry_user.config(fg="#000000")

    def restore_placeholder_user(self, event):
        if self.entry_user.get() == "":
            self.entry_user.insert(0, "Usuario")
            self.entry_user.config(fg="#333333")

    def clear_placeholder_pass(self, event):
        if self.entry_password.get() == "Contraseña":
            self.entry_password.delete(0, 'end')
            self.entry_password.config(show="*", fg="#000000")
            self.password_hidden = True

    def restore_placeholder_pass(self, event):
        if self.entry_password.get() == "":
            self.entry_password.config(show="")
            self.entry_password.insert(0, "Contraseña")
            self.entry_password.config(fg="#333333")
            self.password_hidden = False

    def login(self):
        user = self.entry_user.get()
        password = self.entry_password.get()

        if user == "ADMIN" and password == "1234":
            messagebox.showinfo("Login", "Bienvenido Admin")
            # self.root.destroy()
            # app2 = App()
            # app2.mainloop()
        else:
            messagebox.showerror("ERROR", "Error en sus credenciales, inténtelo de nuevo.")


# Función auxiliar para crear rectángulos redondeados en Canvas
def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, **kwargs, smooth=True)


# Agregar el método al Canvas
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle

# --- BLOQUE PRINCIPAL PARA EJECUTAR ---
if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()