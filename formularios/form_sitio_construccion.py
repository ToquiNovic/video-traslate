import tkinter as tk
import webbrowser
from config import  COLOR_CUERPO_PRINCIPAL
import util.util_imagenes as util_img

def download_pdf():
    url = "https://udlaedu-my.sharepoint.com/personal/j_toquica_udla_edu_co/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fj%5Ftoquica%5Fudla%5Fedu%5Fco%2FDocuments%2FInforme%20Procesamiento%20de%20lenguaje%20natural%2Epdf&parent=%2Fpersonal%2Fj%5Ftoquica%5Fudla%5Fedu%5Fco%2FDocuments&ga=1"
    webbrowser.open(url)

class FormularioSitioConstruccionDesign():

    def __init__(self, panel_principal, logo):

        # Crear paneles: barra superior
        self.barra_superior = tk.Frame( panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        self.barra_inferior = tk.Frame( panel_principal,background=COLOR_CUERPO_PRINCIPAL)
        self.barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        self.labelTitulo = tk.Label(self.barra_superior, text="Documentación")
        self.labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        self.labelTitulo.pack(side=tk.TOP, fill='both', expand=True)
        
        self.label_detail = tk.Label(self.barra_inferior, text="Por favor, si deseas explorar la documentación, haz clic en el botón a continuación. Te llevará a una\n página web donde podrás visualizar el documento y encontrar información detallada sobre nuestro servicio.",
                                     fg="black", font=("Roboto", 14), bg=COLOR_CUERPO_PRINCIPAL,justify="center")
        #self.label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        self.label_detail.pack(side="top",pady=10,padx=10)
        
         # Segundo Label con la imagen
        self.boton = tk.Button(self.barra_inferior,  image=logo, font=("Roboto", 10,"bold"), command=download_pdf, bg=COLOR_CUERPO_PRINCIPAL)
        self.boton.pack(side="top",pady=10)
        
        self.label_imagen = tk.Label(self.barra_inferior,text="⬆️ Descargar ⬆️" , fg="black", font=("Roboto", 14), bg=COLOR_CUERPO_PRINCIPAL)
        self.label_imagen.pack(side="top",pady=10)

       

        