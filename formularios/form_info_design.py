import os
import tkinter as tk
from typing_extensions import Literal
import util.util_ventana as util_ventana

class FormularioInfoDesign(tk.Toplevel):

    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.contruirWidget()

    def config_window(self):
        # Configuración inicial de la ventana
        current_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.title('UdlaMaker')
        self.iconbitmap(os.path.join(current_directory, "imagenes", "logo.ico"))
        w, h = 400, 120        
        util_ventana.centrar_ventana(self, w, h)     
    
    def contruirWidget(self):         
        self.labelVersion = tk.Label(self, text="Version : 1.0")
        self.labelVersion.config(fg="#000000", font=("Roboto", 12, 'bold'))
        self.labelVersion.pack(side='top')
        
        self.labelDetail = tk.Label(self, text="Generar subtítulos con inteligencia artificial,\npartiendo de un video o audio.")
        self.labelDetail.config(fg="#000000", font=("Roboto", 12))
        self.labelDetail.pack(side='top')

        self.labelAutor = tk.Label(self, text="Autores:")
        self.labelAutor.config(fg="#000000", font=( "Roboto", 12,"bold"))
        self.labelAutor.pack(side='top')
        
        self.labelAutor1 = tk.Label(self, text="Daniel Toquica & Carlos Ortiz")
        self.labelAutor1.config(fg="#000000", font=( "Roboto", 12))
        self.labelAutor1.pack(side='top')

