import tkinter as tk
import subprocess
import os
""" import whisper """
import webbrowser
from moviepy.config import change_settings
from moviepy.video.tools.subtitles import file_to_subtitles, SubtitlesClip
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from matplotlib.figure import Figure
from tkinter import Label, Button, StringVar, OptionMenu, Frame, ttk, Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.ttk import Combobox, Style
from tkinter.filedialog import askopenfilename
from formularios.form_error import ModalError
from tkinter import messagebox
from tkinter import filedialog
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA

change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

os.environ["FFMPEG_BINARY"] = r"C:/ProgramData/chocolatey/bin/ffmpeg.exe"

class FormularioGraficasDesign():
    def __init__(self, panel_principal):                   
        panelIzq = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        panelIzq.pack(side='left', fill='both',expand=True)  
        
        panelDer = Frame(panel_principal, bg=COLOR_CUERPO_PRINCIPAL)
        panelDer.pack(side='right', fill='both', expand=True) 
        
        # Etiqueta para el idioma
        label_idioma = Label(panelDer, text="Selecciona el idioma de traducción",
                             font=("Roboto", 16, "bold"), fg="black", bg=COLOR_CUERPO_PRINCIPAL)
        label_idioma.pack(side='top', pady=10, padx=10)
        
        # Variable para almacenar el idioma seleccionado
        idioma = StringVar(panelDer)
        idioma.set("Seleccionar") 

         # Opciones para el idioma
        dropdown_options = [
            'Español',
            'Inglés',
            'Francés',
            'Árabe',
            'Bielorruso',
            'Bosnio',
            'Catalán',
            'Alemán',
            'Griego',
            'Persa',
            'Portugués',
            'Finlandés',
            'Gallego',
            'Indonesio',
            'Islandés',
            'Italiano',
            'Japonés',
        ]

        menu_idioma = Combobox(panelDer,textvariable=idioma, values=dropdown_options, 
                                         font=("Roboto", 16),
                                         background=COLOR_CUERPO_PRINCIPAL,
                                         state="readonly")
        menu_idioma.pack(side='top', pady=10, padx=10) 
        
        # Etiqueta para el tipo de archivo
        label_tipo_archivo = Label(panelIzq, text="Selecciona el tipo de archivo", 
                                    font=("Roboto", 16, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black" )
        label_tipo_archivo.pack(side='top', pady=10, padx=10)

        opciones_tipo_archivo = ["Audio", "Video"]
        # Variable para almacenar el tipo de archivo seleccionado
        tipo_archivo = StringVar(panelIzq)
        tipo_archivo.set("Seleccionar") 
        
        select_tipo_archivo = Combobox(panelIzq, textvariable=tipo_archivo, values=opciones_tipo_archivo, 
                                         font=("Roboto", 16),
                                         background=COLOR_CUERPO_PRINCIPAL,
                                         state="readonly")
        select_tipo_archivo.pack(side='top', pady=10, padx=10) 
        menu_tipo_archivo = OptionMenu(panelIzq, tipo_archivo, *opciones_tipo_archivo)
        
        # Etiqueta para el tipo de archivo
        label_archivo = Label(panelIzq, text="Cargue un archivo para comenzar" , font=(
            "Roboto", 16, "bold"), bg=COLOR_CUERPO_PRINCIPAL, fg="black" )
        label_archivo.pack(side='top', pady=10, padx=10)
        
        boton_subir = Button(panelIzq,
                                   text="Subir", bd=0,
                                   font=("Roboto", 16, "bold"),
                                   borderwidth=0, 
                                   relief="flat" ,
                                   command=lambda: mostrar_error_idioma() if idioma.get() == 'Seleccionar' else abrir_archivo_multimedia(idioma,tipo_archivo))
        boton_subir.pack(side='top',pady=10, padx=10,ipady=10, ipadx=40)
        
        def mostrar_error_idioma():
            messagebox.showerror("Error","Por favor, selecciona un idioma.")
            
        def mostrar_error_tipo_archivo():
            messagebox.showerror("Error","Por favor, selecciona un tipo de archivo.")
            
        def abrir_panel_info():           
            ModalError() 
 
        def abrir_archivo_multimedia(idioma,tipo):
            try:
                if(tipo.get().lower() == 'seleccionar'):
                    mostrar_error_tipo_archivo()
                else:
                    Tk().withdraw()
            
                    if tipo.get().lower() == 'audio':
                        archivo = askopenfilename(initialdir="./data", title="Seleccionar archivo de audio", filetypes=(("Archivos de audio", "*.wav"), ("Todos los archivos", "*.*")))
                    else:
                        archivo = askopenfilename(initialdir="./data", title="Seleccionar archivo de video", filetypes=(("Archivos de video", "*.mp4;*.avi"), ("Todos los archivos", "*.*")))
                        
                    if not archivo:
                        messagebox.showerror("Error","No se seleccionó ningún archivo.")
                        return None
                
                    realizar_traduccion(archivo,idioma)
                
                    nombre_archivo_sin_extension = os.path.splitext(os.path.basename(archivo))[0]
                    ruta_subtitulos = f"./data/translate/video.srt"

                    video_original = VideoFileClip(archivo)
                    #video_original = video_original.set_fps(30)
                    subtitles = generar_subtitulos(archivo, ruta_subtitulos)
    
                    crear_video_con_subtitulos(video_original, subtitles)
                    return archivo    
            
            except Exception as e:
                print(f"Error al abrir el archivo multimedia: {e}")
              
        def obtener_tipo_archivo_idioma():
                panelDer.destroy()
    
        def dividir_texto(texto, ancho_disponible, video_ancho):
            palabras = texto.split()
            lineas = []
            linea_actual = ""
            
            for palabra in palabras:
                if TextClip(linea_actual + " " + palabra, fontsize=video_ancho // 20).w > ancho_disponible:
                    lineas.append(linea_actual)
                    linea_actual = palabra
                else:
                    linea_actual += " " + palabra
            
            lineas.append(linea_actual)
            return "\n".join(lineas)          
                    
        def generar_subtitulos(archivo, ruta_subtitulos):
            video_original = VideoFileClip(archivo)
            video_ancho, video_alto = video_original.size 

            def generator(txt):
                return TextClip(dividir_texto(txt, video_ancho, video_ancho), font='Arial', fontsize=video_ancho // 20, color='white')
            
            if os.path.exists(ruta_subtitulos):
                srt_subtitles = file_to_subtitles(ruta_subtitulos)
                subtitles = SubtitlesClip(srt_subtitles, generator)
                return subtitles
            else:
                messagebox.showerror("Error",f"El archivo de subtítulos no existe en la ruta: {ruta_subtitulos}")
            return None

        def crear_video_con_subtitulos(video_original, subtitles):
            print("Creando Video...")
            try:
                video_salida = "video_con_subtitulos.mp4"
                result = CompositeVideoClip([video_original, subtitles.set_position(('center', 'bottom'))])
                
                result.write_videofile(video_salida, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
                
                print(f"Video creado exitosamente: {video_salida}")
                boton_subir.config(state="normal")
                messagebox.showinfo("Información",f"El archivo se genero con éxito")
                abrir_reproductor()

            except Exception as e:
                print(f"Error al escribir el video: {e}")
           
        def realizar_traduccion(archivo, idioma):
            print("Traduciendo...")

            # Deshabilitar el botón mientras se ejecuta la traducción
            boton_subir.config(state="disabled")
            messagebox.showinfo("Información", "La traducción está en progreso. Por favor, espera...", parent=panel_principal)
            
            # Mapeo de nombres de idiomas a códigos
            codigos_idioma = {
                'español': 'es',
                'inglés': 'en',
                'francés': 'fr',
                'árabe': 'ar',
                'bielorruso': 'be',
                'bosnio': 'bs',
                'catalán': 'ca',
                'alemán': 'de',
                'griego': 'el',
                'persa': 'fa',
                'portugués': 'pt',
                'finlandés': 'fi',
                'gallego': 'gl',
                'indonesio': 'id',
                'islandés': 'is',
                'italiano': 'it',
                'japonés': 'ja',
            }

            # Obtener el código del idioma correspondiente o usar inglés como valor predeterminado
            codigo_idioma = codigos_idioma.get(idioma.get(), 'en')
           
            # Comando para la traducción utilizando el tool "whisper"
            comando = f'whisper "{archivo}" --model small --language {codigo_idioma} --output_dir "./data/translate"'

            # Ejecutar el comando en el shell
            with open(os.devnull, 'w') as null:
                result = subprocess.run(comando, shell=True, stdout=null, stderr=null)

            # Verificar si la traducción se realizó con éxito
            if result.returncode == 0:
                print("La traducción se ha completado con éxito.")
            else:
                print("Error en la traducción. Consulte los mensajes de error para obtener más información.")

        def abrir_reproductor():
                video_url = f'file:///Users/caol/Documents/Projects/own/video-traslate/video_con_subtitulos.mp4'
                webbrowser.open(video_url)