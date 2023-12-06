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
        barra_superior = tk.Frame( panel_principal)
        barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False) 

        # Crear paneles: barra inferior
        barra_inferior = tk.Frame( panel_principal,background=COLOR_CUERPO_PRINCIPAL)
        barra_inferior.pack(side=tk.BOTTOM, fill='both', expand=True)  

        # Primer Label con texto
        labelTitulo = tk.Label(barra_superior, text="Documentación")
        labelTitulo.config(fg="#222d33", font=("Roboto", 30), bg=COLOR_CUERPO_PRINCIPAL)
        labelTitulo.pack(side=tk.TOP, fill='both', expand=True)
        
        label_detail = tk.Label(barra_inferior, text="Por favor, si deseas explorar la documentación, haz clic en el botón a continuación. Te llevará a una\n página web donde podrás visualizar el documento y encontrar información detallada sobre nuestro servicio.",
                                     fg="black", font=("Roboto", 14), bg=COLOR_CUERPO_PRINCIPAL,justify="center")
        #label_imagen.place(x=0, y=0, relwidth=1, relheight=1)
        label_detail.pack(side="top",pady=10,padx=10)
        
         # Segundo Label con la imagen
        boton = tk.Button(barra_inferior,  image=logo, font=("Roboto", 10,"bold"), command=download_pdf, bg=COLOR_CUERPO_PRINCIPAL)
        boton.pack(side="top",pady=10)
        
        label_imagen = tk.Label(barra_inferior,text="Descargar" , fg="black", font=("Roboto", 14), bg=COLOR_CUERPO_PRINCIPAL)
        label_imagen.pack(side="top",pady=10)

       

        