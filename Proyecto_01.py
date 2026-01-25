import tkinter as tk
from tkinter import messagebox
import os


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("GEOS - Herramientas y Equipos")
        self.root.geometry("500x600")
        self.root.configure(bg="#FFFFFF")
        self.root.resizable(False, False)

        self.COLOR_FONDO = "#FFFFFF"
        self.COLOR_AZUL = "#0055A5"
        self.COLOR_INPUT_BG = "#F0F8FF"
        self.COLOR_TEXTO = "#333333"

        self.centrar_ventana(500, 600)

        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(ruta_script, "logo_geos.png")

        self.imagen = tk.PhotoImage(file=ruta_logo)
        self.label_logo = tk.Label(self.root, image=self.imagen, bg=self.COLOR_FONDO)
        self.label_logo.pack(pady=(60, 80))

        self.frame_login = tk.Frame(self.root, bg=self.COLOR_FONDO)
        self.frame_login.pack()

        self.frame_user = tk.Frame(self.frame_login, bg=self.COLOR_INPUT_BG,highlightbackground=self.COLOR_AZUL,highlightthickness=2)
        self.frame_user.pack(pady=(0, 20))

        tk.Label(self.frame_user, text="👤", font=("Arial", 14),bg=self.COLOR_INPUT_BG, fg=self.COLOR_AZUL).pack(side="left", padx=(15, 5))

        self.entry_user = tk.Entry(self.frame_user, font=("Arial", 12),bg=self.COLOR_INPUT_BG, fg=self.COLOR_TEXTO,relief="flat", width=28)
        self.entry_user.pack(side="left", padx=(5, 15), pady=15)
        self.entry_user.insert(0, "Usuario")
        self.entry_user.bind("<FocusIn>", self.clear_placeholder_user)
        self.entry_user.bind("<FocusOut>", self.restore_placeholder_user)

        self.frame_pass = tk.Frame(self.frame_login, bg=self.COLOR_INPUT_BG,highlightbackground=self.COLOR_AZUL,highlightthickness=2)
        self.frame_pass.pack(pady=(0, 40))

        tk.Label(self.frame_pass, text="🔒", font=("Arial", 14),bg=self.COLOR_INPUT_BG, fg=self.COLOR_AZUL).pack(side="left", padx=(15, 5))

        self.entry_password = tk.Entry(self.frame_pass, font=("Arial", 12),bg=self.COLOR_INPUT_BG, fg=self.COLOR_TEXTO,relief="flat", width=28)
        self.entry_password.pack(side="left", padx=(5, 15), pady=15)
        self.entry_password.insert(0, "Contraseña")
        self.entry_password.bind("<FocusIn>", self.clear_placeholder_pass)
        self.entry_password.bind("<FocusOut>", self.restore_placeholder_pass)
        self.password_hidden = False

        self.boton_login = tk.Button(self.frame_login, text="INICIAR SESIÓN",bg=self.COLOR_AZUL, fg="white",font=("Arial", 12, "bold"),relief="flat", cursor="hand2",width=32, height=2,command=self.login)
        self.boton_login.pack()

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
            self.entry_user.config(fg="#666666")

    def clear_placeholder_pass(self, event):
        if self.entry_password.get() == "Contraseña":
            self.entry_password.delete(0, 'end')
            self.entry_password.config(show="*", fg="#000000")
            self.password_hidden = True

    def restore_placeholder_pass(self, event):
        if self.entry_password.get() == "":
            self.entry_password.config(show="")
            self.entry_password.insert(0, "Contraseña")
            self.entry_password.config(fg="#666666")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()