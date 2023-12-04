import tkinter as tk
from typing_extensions import Literal
import util.util_ventana as util_ventana

class ModalError(tk.Toplevel):

    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.contruirWidget()

    def config_window(self):
        # Configuración inicial de la ventana
        self.title('UdlaMaker')
        self.iconbitmap("./imagenes/logo.ico")
        w, h = 400, 100        
        util_ventana.centrar_ventana(self, w, h)     
    
    def contruirWidget(self):         
        self.labelVersion = tk.Label(self, text=" el idioma que desea traducir ")
        self.labelVersion.config(fg="#000000", font=(
            "Roboto", 15), pady=10, width=20)
        self.labelVersion.pack()

        self.labelAutor = tk.Label(self, text="No hay idioma seleccionado")
        self.labelAutor.config(fg="#000000", font=(
            "Roboto", 15), pady=10, width=20)
        self.labelAutor.pack()

